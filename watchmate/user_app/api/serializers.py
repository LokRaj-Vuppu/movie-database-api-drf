from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'} ,write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        email = self.validated_data['email']


        if password != password2:
            error = 'Password and Password2 must be same' 
            raise serializers.ValidationError({'error':error})

        if User.objects.filter(email=email).exists():
            error = 'Email already exists!!'
            raise serializers.ValidationError({'error':error})


        account = User(username=username, email=email)
        account.set_password(password)
        account.save()

        return account

        