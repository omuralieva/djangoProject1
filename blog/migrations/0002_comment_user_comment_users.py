# Generated by Django 4.0 on 2021-12-08 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=20, verbose_name='Логин')),
                ('name', models.CharField(max_length=20, verbose_name='Имя')),
                ('comments', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment', verbose_name='Коментарии')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.user', verbose_name='Пользователь'),
        ),
    ]