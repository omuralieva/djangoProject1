from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from blog.models import Category, Post, Author


def index(request):
    categories = Category.objects.all()
    authors = Author.objects.all
    try:
        category_fan = Category.objects.get(title='Фантастика')
    except ObjectDoesNotExist:
        raise ValueError('Такой категории не существует!')
    return render(request, 'index.html', {'categories': categories, 'fan': category_fan, 'authors': authors})


def category(request, pk):
    posts = Post.objects.filter(category_id=pk)
    return render(request, 'category.html', locals())


def author(request, pk):
    posts = Post.objects.filter(author_id=pk)
    params = {posts: 'posts'}
    return render(request, 'author.html', params)
