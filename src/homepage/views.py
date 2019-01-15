from django.shortcuts import render
from django.http import HttpResponse
def homepage_view(request):
	context={}
	return render(request, "Home/home.html", context)