from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models
from rest_framework.authtoken.models import Token


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name='Категория', null=True)
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, verbose_name='Автор', null=True)

    def __str__(self):
        return self.title


class Ad(models.Model):
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='ads/', verbose_name='Главное изображение', null=True, blank=True)
    user = models.ForeignKey(to='CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    moderated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name='Price')
    discount = models.IntegerField(blank=True, null=True, verbose_name='Discount')

    def __str__(self):
        return self.title

    @property
    def get_price(self):
        if self.price and self.discount:
            price = self.price - (self.price * self.discount / 100)
        else:
            price = 'Договорная'
        return price

    def get_remote_image(self, url):
        if not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}.jpeg", File(img_temp))
        self.save()


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')

    def __str__(self):
        return f'{self.name} {self.last_name}'


class CustomUser(AbstractUser):
    username = models.CharField(verbose_name='Логин', max_length=100, unique=True)
    email = models.EmailField(verbose_name='email')
    password = models.CharField(verbose_name='Пароль', max_length=100)
    is_email_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to='CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь', null=True)

    def __str__(self):
        return str(self.user)
