from rest_framework import serializers
from .models import User
from .validators import validate_strong_password

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_strong_password])

    class Meta:
        model = User
        fields = ['email', 'password', 'student_id', 'name', 'major']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
