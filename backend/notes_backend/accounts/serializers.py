from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User  # which model to use to create serializer
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        ]  # which fields should be exposed both sides
        # though password is marked as write_only above.
        # so it doesnt get sent to front end but able to be received for writing.

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
