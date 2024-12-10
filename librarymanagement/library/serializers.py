from rest_framework import serializers
from .models import CustomUser, Book, BorrowRequest
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff']
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']  # Add any fields you need
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures password is write-only
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])  # Set the password securely
        user.save()
        return user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)  # Ensure 'email' is used instead of 'username'

    def validate(self, attrs):
        email = attrs.get('email', None)  # Expect 'email' in the request
        password = attrs.get('password', None)
        
        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        # Use email to authenticate the user
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        # If email and password are correct, return the token
        return super().validate(attrs)

class BookSerializer(serializers.ModelSerializer):
    available_copies = serializers.IntegerField(required=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'available_copies']

class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['id', 'user', 'book', 'borrow_date', 'return_date', 'status']

class BorrowHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowHistory
        fields = "__all__"
