from django.core.exceptions import ObjectDoesNotExist

from blog.models import Category, Author, User, Comment


def asd(request):
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

    params = {'categories': categories, 'fan': category_fan, 'authors': authors,
              'users': usr}
    return params
