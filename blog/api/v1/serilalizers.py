
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from blog.models import Ad, CustomUser


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('id', 'title', 'price', 'description', 'image', 'created_at', 'moderated', 'is_active')

    def get_price(self, obj):
        return obj.get_price

    def get_user_name(self, obj):
        return obj.user.username

    def create(self, validated_data):
        moderated = validated_data.pop('moderated')
        instance = Ad.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        if validated_data.get('price') > 0:
            instance.price = validated_data.get('price')
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({"error": 'price is not valid'})


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']

    def save(self, **kwargs):
        user = CustomUser(username=self.validated_data['username'],
                          email=self.validated_data['email'],
                          )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise ValidationError('password didnt exist')

        user.set_password(password)
        user.save()
        return user


