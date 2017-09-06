from django.db.models import Q
from knox.models import AuthToken
from rest_framework import serializers

from users.models import UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)

    def create(self, validated_data):
        user = UserProfile(email=validated_data['email'])
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    token = serializers.CharField(read_only=True, allow_blank=True)
    first_name = serializers.CharField(read_only=True, allow_blank=True)
    last_name = serializers.CharField(read_only=True, allow_blank=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        user_obj = None
        username = attrs.get('username')
        email = attrs.get('username')
        password = attrs.get('password')

        if not any([username, email]):
            raise serializers.ValidationError('A username or email is required...')

        user = UserProfile.objects.filter(Q(email=email) | Q(username=username)).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        if user_obj:
            if user_obj.check_password(password):
                attrs['username'] = user_obj.username
                attrs['email'] = user_obj.email
                token = AuthToken.objects.create(user_obj)
                attrs['token'] = token
                return attrs

        raise serializers.ValidationError('Password Validation Failed...')

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'token')

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
