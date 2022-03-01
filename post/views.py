from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from post.models import Post


def detail(request, post_id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(id=post_id)
            values = {'author': post.author.username}
            values.update(post.__dict__)
            return render(request, 'post/post_detail.html', values)
        except Post.DoesNotExist:
            return HttpResponseNotFound()
    return HttpResponseNotAllowed('GET')


def write(request):
    user = request.user
    if not user.is_authenticated:
        # TODO: change this redirects to login page
        return HttpResponseForbidden()

    if request.method == 'GET':
        return render(request, 'post/post_write.html')
    elif request.method == 'POST':
        try:
            created_post = Post.objects.create(
                title=request.POST['input_title'],
                content=request.POST['input_content'],
                author=request.user,
            )
        except KeyError:
            return HttpResponseBadRequest()
        return redirect('post_detail', post_id=created_post)
