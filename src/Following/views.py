import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from .models import FollowModel
from .forms import FollowForm
from .managers import FollowManager


User = get_user_model()


@login_required
def show_follower(request, following_id):
	follower_list = FollowModel.follow_shortcuts.get_follower_list(
		following_id)
	request_id = request.user.id
	request_following_list = FollowModel.follow_shortcuts.get_following_list(
		request_id)
	request_following_ids = request_following_list.values_list(
		'following_id', 
		flat=True
		)
	request_follows = follower_list.filter(
		follower_id__in=request_following_ids)
	request_not_follows = follower_list.exclude(
		follower_id__in=request_following_ids)
	context = dict(
	page_owner=User.objects.get(id=following_id),
	form=FollowForm,
	request_follows=request_follows,
	request_not_follows=request_not_follows
	)
	return render(request, 'Following/follower.html',context)

	
def show_following(request, follower_id):
	following_list = FollowModel.follow_shortcuts.get_following_list(
		follower_id)
	request_id = request.user.id
	request_following_list = FollowModel.follow_shortcuts.get_following_list(
		request_id)
	request_following_ids = request_following_list.values_list(
		'following_id', 
		flat=True
		)
	request_follows = following_list.filter(
		following_id__in=request_following_ids)
	request_not_follows = following_list.exclude(
		following_id__in=request_following_ids)
	context = dict(
	page_owner=User.objects.get(id=follower_id),
	form=FollowForm,
	request_follows=request_follows,
	request_not_follows=request_not_follows
	)
	return render(request, 'Following/following.html',context)


@login_required
def do_follow(request, buttonuser_id):
	follower_id = request.user.id
	following_id = int(buttonuser_id)
	if request.method == "POST":
		form = FollowForm(request.POST)
		if form.is_valid():
			filtered_relation = \
			FollowModel.follow_shortcuts.get_follow_relation(
				follower_id, buttonuser_id
				)
			if filtered_relation.exists() == True:
			    delete_object = filtered_relation.delete()
			else:
				try:
					follow = FollowModel(
						follower_id = follower_id,
						following_id = following_id,
						following_since = datetime.datetime.now(),
						)
					follow.save()
				except ValueError as e:
					messages.error(request, 'You cannot follow yourself!!')
		else:
			print('form not valid')
	next = request.POST.get('next', '/')
	return HttpResponseRedirect(next)