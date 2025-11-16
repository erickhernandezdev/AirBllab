import json
import uuid
import logging
import os
import re

from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from fido2.server import Fido2Server
from fido2.utils import websafe_encode, websafe_decode
from fido2.webauthn import (AttestedCredentialData, PublicKeyCredentialUserEntity, AuthenticatorAttachment,)

from multifactor.factors.fido2 import FidoClass
from multifactor.models import UserKey, KeyTypes
from multifactor.common import write_session, login as mf_login

logger = logging.getLogger(__name__)


def _allowed_aaguids():
  # Leer allowlist de MULTIFACTOR settings
  mf = getattr(settings, 'MULTIFACTOR', {}) or {}
  return set((mf.get('ALLOWED_AAGUIDS') or []))


def _format_aaguid(aaguid_bytes: bytes) -> str:
  try:
    return str(uuid.UUID(bytes=aaguid_bytes))
  except Exception:
    return aaguid_bytes.hex()


def _auto_add_aaguid_to_settings(aaguid: str):
  """
  Modo aprendizaje: auto-añade la primera AAGUID a ALLOWED_AAGUIDS en settings.py
  si la lista está vacía. Esto permite que la primera YubiKey registrada sea
  automáticamente aceptada y las demás queden bloqueadas hasta añadirlas manualmente.
  """
  try:
    settings_path = os.path.join(settings.BASE_DIR, 'airbnb_app', 'settings.py')
    if not os.path.exists(settings_path):
      logger.error("No se pudo localizar settings.py para auto-aprendizaje AAGUID")
      return False

    with open(settings_path, 'r', encoding='utf-8') as f:
      content = f.read()

    # Buscar la sección ALLOWED_AAGUIDS (vacía o con comentarios)
    # Patrón: 'ALLOWED_AAGUIDS': [ ... ]
    pattern = r"('ALLOWED_AAGUIDS'\s*:\s*\[)(.*?)(\])"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
      logger.warning("No se encontró 'ALLOWED_AAGUIDS' en settings.py")
      return False

    before, existing, after = match.groups()
    # Si ya hay AAGUIDs (no vacío, ignorando comentarios y espacios), no sobrescribir
    cleaned = re.sub(r'#.*', '', existing).strip()
    if cleaned and cleaned != ',':
      logger.info("ALLOWED_AAGUIDS ya contiene entradas; no auto-añadiendo.")
      return False

    # Insertar el AAGUID
    new_content = content[:match.start()] + f"{before}\n        '{aaguid}',  # Auto-aprendido\n    {after}" + content[match.end():]

    with open(settings_path, 'w', encoding='utf-8') as f:
      f.write(new_content)

    logger.info("AAGUID %s auto-añadido a ALLOWED_AAGUIDS en settings.py", aaguid)
    # Actualizar settings en memoria (opcional; requiere reload del módulo, pero al menos loguea)
    if hasattr(settings, 'MULTIFACTOR') and isinstance(settings.MULTIFACTOR, dict):
      if 'ALLOWED_AAGUIDS' not in settings.MULTIFACTOR:
        settings.MULTIFACTOR['ALLOWED_AAGUIDS'] = []
      settings.MULTIFACTOR['ALLOWED_AAGUIDS'].append(aaguid)
    return True

  except Exception:
    logger.exception("Error auto-añadiendo AAGUID a settings.py")
    return False


class YubiFidoBase(FidoClass):
  @property
  def server(self):
    # Forzar preferencia
    return Fido2Server(
      rp=dict(
        id=self.request.get_host().split(":")[0],
        name=settings.MULTIFACTOR.get('FIDO_SERVER_NAME', 'Airbnb CR'),
      ),
        attestation='direct',
    )


@method_decorator(csrf_exempt, name='dispatch')
class YubiRegister(YubiFidoBase):
  def get(self, request, *args, **kwargs):
    # Solo permitir registro de YubiKeys (cross-platform)
    registration_data, state = self.server.register_begin(
      user=PublicKeyCredentialUserEntity(
        id=request.user.get_username().encode('utf-8'),
        name=f'{request.user.get_full_name()}',
        display_name=request.user.get_username(),
      ),
      credentials=self.get_user_credentials(),
      user_verification='required',
      authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
    )
    request.session['fido_state'] = state
    return JsonResponse({**registration_data}, safe=False)

  def post(self, request, *args, **kwargs):
    try:
      data = json.loads(request.body)
      auth_data = self.server.register_complete(
        request.session['fido_state'], data
      )

      aaguid = _format_aaguid(auth_data.credential_data.aaguid)
      allow = _allowed_aaguids()
      
      # Modo aprendizaje: si no hay allowlist, auto-añadir la primera AAGUID
      if not allow:
        logger.info("ALLOWED_AAGUIDS vacía. Auto-aprendiendo primera AAGUID: %s", aaguid)
        success = _auto_add_aaguid_to_settings(aaguid)
        if success:
          messages.info(request, f'Primera YubiKey aprendida (AAGUID: {aaguid}). Reinicia el servidor para que otras llaves queden bloqueadas.')
        else:
          logger.warning("No se pudo auto-añadir AAGUID; procede sin allowlist.")
      elif aaguid not in allow:
        logger.warning("Blocked FIDO2 registration. AAGUID %s not in allowlist", aaguid)
        return JsonResponse({
          'status': 'ERR',
          'message': f'Este autenticador no está permitido. Solo YubiKeys con AAGUID aprobado. AAGUID detectado: {aaguid}',
          'aaguid': aaguid,
        }, status=400)

      encoded = websafe_encode(auth_data.credential_data)
      key = UserKey.objects.create(
        user=request.user,
        properties={
          'device': encoded,
          'type': data['type'],
          'domain': self.server.rp.id,
          'aaguid': aaguid,
        },
        key_type=str(KeyTypes.FIDO2),
      )
      write_session(request, key)
      messages.success(request, 'FIDO2 YubiKey agregada correctamente!')
      return JsonResponse({'status': 'OK'})

    except Exception as e:
      logger.exception("Error completing YubiKey-only registration.")
      return JsonResponse({
        'status': 'ERR',
        'message': 'Error en el servidor, intenta más tarde',
      }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class YubiAuthenticate(YubiFidoBase):
  def get(self, request, *args, **kwargs):
    auth_data, state = self.server.authenticate_begin(
      credentials=self.get_user_credentials(),
      user_verification='required',
    )
    request.session['fido_state'] = state
    return JsonResponse({**auth_data})

  def post(self, request, *args, **kwargs):
    data = json.loads(request.body)
    cred = self.server.authenticate_complete(
      request.session.pop('fido_state'),
      self.get_user_credentials(),
      data,
    )

    allow = _allowed_aaguids()

    keys = UserKey.objects.filter(
      user=request.user,
      key_type=str(KeyTypes.FIDO2),
      enabled=True,
    )

    for key in keys:
      acd = AttestedCredentialData(websafe_decode(key.properties['device']))
      if acd.credential_id == cred.credential_id:
        # Enforzar allowlist de AAGUIDs
        aaguid = _format_aaguid(acd.aaguid)
        if allow and aaguid not in allow:
          logger.warning("Blocked FIDO2 auth. AAGUID %s not allowed", aaguid)
          return JsonResponse({
            'status': 'ERR',
            'message': 'Este autenticador no está permitido.',
          }, status=403)
        write_session(request, key)
        res = mf_login(request)
        return JsonResponse({'status': 'OK', 'redirect': res['location']})

    return JsonResponse({'status': 'ERR'}, status=400)
