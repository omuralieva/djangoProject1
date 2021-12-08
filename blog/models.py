from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name='Категория', null=True)
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, verbose_name='Автор', null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')

    def __str__(self):
        return f'{self.name} {self.last_name}'


class User(models.Model):
    login = models.CharField(max_length=20, verbose_name='Логин')
    name = models.CharField(max_length=20, verbose_name='Имя')

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='Пользователь', null=True)

    def __str__(self):
        return self.text
