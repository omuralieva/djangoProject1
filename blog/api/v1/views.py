from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from blog.api.v1.serilalizers import AdSerializer, CustomUserRegisterSerializer
from blog.models import Ad, CustomUser
from blog.api.v1.utils import generate_token


class ListCreateAdView(ListCreateAPIView):
    queryset = Ad.objects.filter(moderated=True)
    serializer_class = AdSerializer
    pagination_class = PageNumberPagination

    # permission_classes = [IsUserIsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = AdSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=1)
            return Response(serializer.data)


class RetrieveUpdateDestroyAdView(RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def put(self, request, *args, **kwargs):
        data = self.request.data
        pk = data.get('id')
        if pk:
            instance = get_object_or_404(Ad, id=pk)
            price = data.get('price')
            if int(price) > 0:
                instance.price = data.get('price')
                instance.save()
                return Response(AdSerializer(instance).data)
            else:
                return JsonResponse({"error": 'price can not be negative'}, status=HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({"sad": 'object does not exists'})


@api_view(['GET', 'POST'])
def get_list_ads(request, *args, **kwargs):
    ads = Ad.objects.all()
    serializer = AdSerializer(ads, many=True)
    if request.method == 'POST':
        data = request.data
        serializer = AdSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    return Response({'ads': serializer.data})


class CustomUserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'User': 'not found'})
        user = serializer.validated_data['user']
        token = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class CustomUserRegisterView(views.APIView):

    def get(self, *args, **kwargs):
        return Response({'data': {
            'username': 'user',
            'email': 'email',
            'password': 'password',
            'password2': 'password2'

        }})

    def post(self, request, *args, **kwargs):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Активируйте свой аккаунт'
            email_body = render_to_string('activate.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            to_email = serializer.data['email']
            email = EmailMessage(subject=email_subject, body=email_body,
                                 from_email=settings.EMAIL_FROM_USER,
                                 to=[to_email]
                                 )
            email.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activation_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
