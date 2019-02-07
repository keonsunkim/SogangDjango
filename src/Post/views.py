from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from .models import GeneralPost, Tag, FilterTagRelation
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission
from django.contrib.auth import get_user_model
from .forms import GeneralPostCreateAlterForm, GeneralPostDeleteForm
from . import urls
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def post_detail_view(request, post_id):
	if request.method == "POST":
		return HttpResponse(status=400)
	else:
	    post = get_object_or_404(GeneralPost, id=post_id)
	    delete_form = GeneralPostDeleteForm()
	    context = dict()
	    context["post"] = post
	    context["delete_form"] = delete_form
	    return render(request, "posts/detail.html", context)

def post_list_view(request):
	post_list = GeneralPost.objects.all()
	paginator = Paginator(post_list, 6)

	page = request.GET.get('page')

	try: 
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request,"posts/list.html", {'posts':posts})

@login_required
def post_create_view(request):
	if request.method == "POST":
		create_form = GeneralPostCreateAlterForm(request.POST)
		print(request.POST)
		if create_form.is_valid():
			print("I'm valid")
			post = GeneralPost(
				author = request.user,
				title = create_form.cleaned_data['title'],
				content = create_form.cleaned_data['content']
				)
			if "publish" in request.POST:
				post.published = True
			elif "save" in request.POST:
				post.published = False
			post.save()

			for tag in create_form.cleaned_data['tag']:
				tag_obj, created = Tag.objects.get_or_create(name=tag[1:], slug=tag[1:])
				FilterTagRelation.objects.get_or_create(filter_tag_id=tag_obj.id, general_post_id=post.id)
				return redirect(reverse_lazy('posts:detail', kwargs={"post_id":post.id}))

		else:
			return render(request, 'posts/create.html', {'create_form': create_form})
	else:
		create_form = GeneralPostCreateAlterForm()		
	return render(request, 'posts/create.html', {'create_form': create_form})


# @login_required	
# def post_publish_view(request):
	
# 	return redirect("posts:list") 


@login_required
def post_edit_view(request,user_id):
	if user_id == GeneralPost.author_id :
		return render (request,'posts/edit.html')
	
	else :
		return HttpResponse("<script>alert('잘못된 접근입니다.')</script>")

@login_required
def post_delete_view(request, post_id):
	if request.method == "POST":
		delete_form = GeneralPostDeleteForm(request.POST)
		if delete_form.is_valid():
			del_post = get_object_or_404(GeneralPost, id=post_id)
			if del_post.author_id == request.user.id:
				del_post.delete()
			else:
				return HttpResponse(status=403)
		else:
			return HttpResponse(status=400)
	else:
		delete_form = GeneralPostDeleteForm()
	return redirect('/posts/list/')
 

@require_http_methods(["GET","POST"])
def user_post_list(request, user_id):
 	if request.method == "GET":
 		Post.objects.filter(author_id=user_id)
 		context = {'user_post_list': user_post_list
 		}
 		return render(request,'posts/user_post_list.html',context)

 	else:
 		raise Http405

@login_required
def post_edit_view(request, post_id):
	edit_post = get_object_or_404(GeneralPost, id=post_id)
	if edit_post.author_id == request.user.id:
		if request.method == "POST":
			edit_form = GeneralPostCreateAlterForm(request.POST)
			if edit_form.is_valid():
				edit_post.save()
				after_tags = {tag[1:] for tag in edit_form.cleaned_data['tag']}
				before_tags = {tag.filter_tag.name for tag in FilterTagRelation.objects.select_related.filter(general_post_id=post_id)}
				for tag in after_tags.difference(before_tags):
					tag_obj, created = Tag.objects.get_or_create(name=tag, slug=tag)
					FilterTagRelation.objects.get_or_create(filter_tag_id=tag_obj.id, general_post_id=post.id)
				for tag in before_tags.difference(after_tags):
					FilterTagRelation.objects.delete(filter_tag_id=tag_obj.id, general_post_id=post.id)
				return redirect(reverse_lazy('posts:detail', kwargs={"post_id":post.id}))
			else:
				return render(request, 'posts/create.html',{'edit_form' : edit_form})
		else:
			edit_form = GeneralPostCreateAlterForm(initial={'title':title,'content':content,'tag':tag})
			return render(request, 'posts/create.html',{'edit_form' : edit_form})
	else:
		return HttpResponse(status=403)
	


