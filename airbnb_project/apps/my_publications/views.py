from django.shortcuts import render

def my_publications(request):
  return render(request, 'my_publications/my_publications.html')
