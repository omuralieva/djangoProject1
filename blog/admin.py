from django.contrib import admin
from blog.models import Post, Author, Category, User, Comment

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Comment)