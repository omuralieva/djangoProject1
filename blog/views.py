from django.http import HttpResponse
from django.shortcuts import render

from blog.forms import AdForm
from blog.models import Category, Post, Author, Comment, CustomUser, Ad


def index(request):
    categories = Category.objects.all()
    authors = Author.objects.all()
    users = CustomUser.objects.all()

    user_list = []
    for i in users:
        comment = Comment.objects.filter(user_id=i.id)
        if comment:
            user_list.append(i.id)
    usr = users.filter(id__in=user_list)

    params = {'categories': categories, 'authors': authors,
              'users': usr}
    return render(request, 'index.html', params)


def category(request, pk):
    posts = Post.objects.filter(category_id=pk)
    return render(request, 'category.html', locals())


def author(request, pk):
    posts = Post.objects.filter(author_id=pk)
    return render(request, 'author.html', locals())


def user(request, pk):
    comments = Comment.objects.filter(user_id=pk)
    return render(request, 'user.html', locals())


def create_ad(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AdForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                Ad.objects.create(title=cd['title'], description=cd['description'], image=cd['image'],
                                  user=request.user)
                return HttpResponse('Объявление успешно создано!')
        else:
            form = AdForm()
    else:
        return HttpResponse('Вы не авторизованы')
    return render(request, 'ad.html', {'form': form})


def ad_list(request):
    search_query = request.GET.get('query', '')
    if search_query:
        adverts = Ad.objects.filter(title__icontains=search_query)
    else:
        adverts = Ad.objects.all()
    return render(request, 'ad_list.html', {'adverts': adverts})


def ad_detail(request, pk):
    ad = Ad.objects.get(pk=pk)
    return render(request, 'ad_detail.html', {'advert': ad})
