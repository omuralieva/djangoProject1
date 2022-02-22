import csv

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

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


def read_csv(request):
    file = str(settings.BASE_DIR) + r'/blog/parser/ads.csv'
    with open(file, 'r', encoding='utf-8') as f:
        for i in csv.reader(f):
            if i:
                title = i[0]
                desc = i[3]
                image = i[4]
                user_id = 1
                ad = Ad.objects.filter(title=title).exists()
                if not ad:
                    ad = Ad.objects.create(title=title, description=desc, user_id=user_id)
                    if image:
                        ad.get_remote_image(image)
    return HttpResponse('Успешно!')


# class CustomUserDetailView(DetailView):
#
#     context_object_name = 'user'
#     queryset = CustomUser.objects.all()


class AdUserListView(ListView):
    template_name = 'ad_list.html'
    context_object_name = 'adverts'

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, name=self.kwargs['pk'])
        return Ad.objects.filter(user=self.user)
