class DataBaseRouter:
    def db_user(self, model, **hints):
        return 'airbnb_user'

    def db_admin(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'