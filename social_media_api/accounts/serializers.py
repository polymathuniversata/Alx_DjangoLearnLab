from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        
        return token


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'bio', 'profile_picture', 'date_of_birth', 'location', 'website']
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2',
                  'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 from the data
        validated_data.pop('password2', None)
        user = get_user_model().objects.create_user(**validated_data)
        # Create token for the user
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login with token authentication."""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for password change endpoint."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
