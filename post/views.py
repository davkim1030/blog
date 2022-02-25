from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
from django.shortcuts import render

from post.models import Post


def detail(request, post_id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(id=post_id)
            values = {'author': post.author.username}
            values.update(post.__dict__)
            return render(request, 'post_detail.html', values)
        except Post.DoesNotExist as e:
            return HttpResponseNotFound()
    return HttpResponseNotAllowed('GET')
