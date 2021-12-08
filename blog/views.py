
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from blog.models import Category, Post, Author, Comment, User


def index(request):
    categories = Category.objects.all()
    authors = Author.objects.all()
    users = User.objects.all()

    user_list = []
    for i in users:
        comment = Comment.objects.filter(user_id=i.id)
        if comment:
            user_list.append(i.id)
    usr = users.filter(id__in=user_list)

    try:
        category_fan = Category.objects.get(title='Фантастика')
    except ObjectDoesNotExist:
        raise ValueError('Такой категории не существует!')
    return render(request, 'index.html', {'categories': categories, 'fan': category_fan, 'authors': authors,
                                          'users': usr})


def category(request, pk):
    posts = Post.objects.filter(category_id=pk)
    return render(request, 'category.html', locals())


def author(request, pk):
    posts = Post.objects.filter(author_id=pk)
    return render(request, 'author.html', locals())


def user(request, pk):
    comments = Comment.objects.filter(user_id=pk)
    return render(request, 'user.html', locals())
