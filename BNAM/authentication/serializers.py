from User.models import UserProfile
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} 
    def create(self, validated_data): 

        try:
            validate_password(validated_data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        password = make_password(validated_data['password'])

        user = UserProfile.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )
        return user