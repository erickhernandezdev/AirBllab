from django.shortcuts import render

def history_view(request):
    return render(request, 'history.html')
