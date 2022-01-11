from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from blog.registration import log_in, registration
from blog.views import index, category, author, user, create_ad, advert, ad_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('category/<int:pk>', category, name='category'),
    path('author/<int:pk>', author, name='author'),
    path('user/<int:pk>', user, name='user'),
    path('login/', log_in, name='login'),
    path('registration/', registration, name='registration'),
    path('create-ad/', create_ad, name='create_ad'),
    path('advert/', advert, name='advert'),
    path('ad-detail/<int:pk>', ad_detail, name='ad_detail'),






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
