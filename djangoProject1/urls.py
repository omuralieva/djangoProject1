from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path

from blog.api.v1.views import ListCreateAdView, RetrieveUpdateDestroyAdView, CustomUserRegisterView, \
    CustomUserLoginView, activation_user
from blog.registration import log_in, registration, activate_user
from blog.views import index, category, author, user, create_ad, ad_detail, read_csv, AdUserListView, ad_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('category/<int:pk>', category, name='category'),
    path('author/<int:pk>', author, name='author'),
    path('user/<int:pk>', user, name='user'),
    path('login/', log_in, name='login'),
    path('registration/', registration, name='registration'),
    path('create-ad/', create_ad, name='create_ad'),
    path('ad-list/', ad_list, name='ad_list'),
    path('ad-detail/<int:pk>', ad_detail, name='ad_detail'),
    path('activate/<uid64>/<token>', activate_user, name='activate'),
    path('readcsv', read_csv, name='parser'),
    # path('api/v1/get-ads/', get_list_ads, name='get_list_ads'),
    path('ads/user/<int:pk>', AdUserListView.as_view(), name='user_ads'),
    path('api/v1/get-ads/', ListCreateAdView.as_view(), name='get_list_ads'),
    path('api/v1/get-ad/<int:pk>/', RetrieveUpdateDestroyAdView.as_view(), name='get_rud'),
    path('api/v1/register/', CustomUserRegisterView.as_view(), name='registration'),
    path('api/v1/login/', CustomUserLoginView.as_view(), name='login'),
    path('api/v1/activate/<uid64>/<token>', activation_user, name='activation'),






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
