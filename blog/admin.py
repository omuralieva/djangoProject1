from django.contrib import admin
from blog.models import Post, Author, Category

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
