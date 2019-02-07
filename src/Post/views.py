from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import redirect
from .models import GeneralPost,Tag, FilterTagRelation
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import GeneralPostCreateAlterForm,GeneralPostDeleteForm
from django.conf.urls import url
from django.urls import reverse
from django.urls import reverse_lazy

User = get_user_model()

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
	return render(request,'post/user_post_list.html',{'delete_form': delete_form})


@login_required
def post_edit_view(request, post_id):
	if request.method == "POST":
		edit_post = get_object_or_404(GeneralPost, id=post_id)
		edit_form = GeneralPostCreateAlterForm(request.POST, instance=edit_post)
		context = dict(edit_post=edit_post, edit_form=edit_form)
		if edit_form.is_valid():
			print("form is valid")
			if edit_post.author_id == request.user.id:
				print("correct user")
				edited_post = edit_form.save()
				for tag in edit_form.cleaned_data['tag']:
					tag_obj, created = Tag.objects.get_or_create(name=tag[1:],slug=tag[1:])
					FilterTagRelation.objects.get_or_create(filter_tag_id=tag_obj.id,general_post_id=edited_post.id)
				return redirect(reverse_lazy('posts:detail', kwargs={"post_id":edited_post.id}))
			else:
				return HttpResponse(status=403)
		else:
			return render(request, 'post/edit.html', context)
	else:
		edit_post = get_object_or_404(GeneralPost, id=post_id)
		edit_tag = get_object_or_404(FilterTagRelation, general_post_id=post_id)
		
		edit_form = GeneralPostCreateAlterForm(
			initial={'title':edit_post.title,'content':edit_post.content})
		context = dict(edit_post=edit_post, edit_form=edit_form)
		return render(request, 'post/edit.html', context)




def tag_related_post_list_view(request,tag_slug):
	if request.method == "POST":
		return HttpResponse(status=400)
	else:
		tag_model = get_object_or_404(Tag, slug=tag_slug)
		related_post_objects = FilterTagRelation.objects.filter(filter_tag_id=tag_model.id)
		context = dict(related_post_objects=related_post_objects)
		return render (request,"post/tag_related_post_list.html", context)
	   



def post_detail_view(request, post_id):
	if request.method == "POST":
		return HttpResponse(status=400)
	else:
		post = get_object_or_404(GeneralPost,id=post_id)
		
		tags = FilterTagRelation.objects.filter(general_post_id=post_id)
		delete_form = GeneralPostDeleteForm()
		edit_form = GeneralPostCreateAlterForm()
		context = dict()
		context["post"] = post
		context["delete_form"] = delete_form
		context["tags"] = tags
		context["edit_form"] = edit_form
		return render (request,"post/detail.html", context)
	   

def post_list_view(request):
	user=request.user
	post_list = GeneralPost.objects.all()
	paginator = Paginator(post_list, 6)
	page = request.GET.get('page')
	try: 
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	context = {
		"posts":posts
	}
	return render(request,"post/list.html",context)



# def post_list_view(request):
# 	post_list = GeneralPost.objects.all()
# 	paginator = Paginator(post_list, 6)

# 	page = request.GET.get('page')

# 	try: 
# 		posts = paginator.page(page)
# 	except PageNotAnInteger:
# 		posts = paginator.page(1)
# 	except EmptyPage:
# 		posts = paginator.page(paginator.num_pages)

# 	return render(request,"posts/list.html", {'posts':posts})


@require_http_methods(["GET","POST"])
def user_post_list_view(request):
	if request.method == "GET":
		user=request.user
		user_posts= GeneralPost.objects.filter(author_id=user.id)
		context = {'user_posts': user_posts
		}
		return render(request,'post/user_post_list.html',context)
	else:
		raise Http405

		
@require_http_methods(["GET","POST"])
def author_post_list_view(request, author_slugname):
	if request.method == "GET":
		author =get_object_or_404(User, slug_name_for_url = author_slugname)
		author_posts = GeneralPost.objects.filter(author_id=author.id)
		return render(request,'post/author_post_list.html', { 'author_posts': author_posts })
	else:
		raise Http405

	
@login_required
def post_create_view(request):
	if request.method == "POST":
		print(request.POST)
		form = GeneralPostCreateAlterForm(request.POST)
		if form.is_valid():
			post = GeneralPost(
				author = request.user,
				title = form.cleaned_data['title'],
				content = form.cleaned_data['content'],
				)
			if "publish" in request.POST:
				post.published = True

			elif "save" in request.POST:
				post.published = False
			post.save()
			for tag in form.cleaned_data['tag']:
				tag_obj, created = Tag.objects.get_or_create(name=tag[1:],slug=tag[1:])
				FilterTagRelation.objects.get_or_create(filter_tag_id=tag_obj.id,general_post_id=post.id)
				return redirect(reverse_lazy('posts:detail', kwargs={"post_id":post.id}))
		else :
			return render(request,'post/create.html', {'form': form})
	else:
		form = GeneralPostCreateAlterForm()
	return render(request,'post/create.html', {'form': form})













