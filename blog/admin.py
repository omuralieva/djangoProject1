from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models import Post, Author, Category, CustomUser, Comment, Ad


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_premium', 'is_email_verified', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_premium')


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'title', 'user', 'is_active', 'moderated')
    list_filter = ['user', 'created_at']
    search_fields = ['description__startswith', 'title__startswith']
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
