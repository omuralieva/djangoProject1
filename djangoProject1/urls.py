from django.contrib import admin
from django.urls import path
from blog.views import index, category, author, user, registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('category/<int:pk>', category, name='category'),
    path('author/<int:pk>', author, name='author'),
    path('user/<int:pk>', user, name='user'),




]
