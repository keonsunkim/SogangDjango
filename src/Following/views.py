from django.shortcuts import render
from django.http import HttpResponse

from .models import Following
def index(request):
	return HttpResponse("Hello, you have entered 'Follow'.")

def show_follower(request, followed_id):
	follower_list = Following.objects.filter(followed_id = followed_id)
	follower_sample = follower_list.order_by("?").first()
	context = {
	'follower_sample': follower_sample,
	'follower_list': follower_list}
	return render(request, 'Following/follower.html',context)
	
def show_following(request, follower_id):
	following_list = Following.objects.filter(follower_id = follower_id)
	following_sample = following_list.order_by("?").first()
	context = {
	'following_sample': following_sample,
	'following_list': following_list
	}
	return render(request, 'Following/following.html',context)