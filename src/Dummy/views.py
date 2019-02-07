from django.shortcuts import render

from django.contrib.auth import get_user_model

User = get_user_model()


def dummy_base_view(request):
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        context = dict()
        context['user'] = user
        return render(request, 'dummy/base.html', context)
    else:
        return render(request, 'dummy/base.html', dict())


def dummy_home_view(request):
    return render(request, 'dummy/home.html', dict())
