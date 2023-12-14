from rest_framework import serializers
import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.constants import PASSWORD_MATCH_ERROR, \
    CONTACT_NUMBER_VALUE_ERROR, CONTACT_NUMBER_LENGTH_ERROR, CONTACT_NUMBER_ALREADY_EXIST_ERROR
from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('name', 'password', 'password2',
                  'email', 'contact_number')

    def validate_contact_number(self, value):
        # contact number should have at least 10 digits
        if len(value) != 10:
            raise serializers.ValidationError(CONTACT_NUMBER_LENGTH_ERROR)

        if not re.match("^[0-9]+$", value):
            raise serializers.ValidationError(CONTACT_NUMBER_VALUE_ERROR)

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": PASSWORD_MATCH_ERROR})
        existing_users = User.objects.filter(
            contact_number=attrs['contact_number']
        )
        if self.instance:
            existing_users = existing_users.exclude(pk=self.instance.pk)

        if existing_users.exists():
            raise serializers.ValidationError(CONTACT_NUMBER_ALREADY_EXIST_ERROR)
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            contact_number=validated_data['contact_number']

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ObtainTokenSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('name', 'contact_number', 'email')

    def validate_contact_number(self, value):
        # contact number should have at least 10 digits
        if len(value) != 10:
            raise serializers.ValidationError(CONTACT_NUMBER_LENGTH_ERROR)

        if not re.match("^[0-9]+$", value):
            raise serializers.ValidationError(CONTACT_NUMBER_VALUE_ERROR)

        return value

    def validate(self, attrs):

        existing_users = User.objects.filter(
            contact_number=attrs['contact_number']
        )
        if self.instance:
            existing_users = existing_users.exclude(pk=self.instance.pk)

        if existing_users.exists():
            raise serializers.ValidationError(CONTACT_NUMBER_ALREADY_EXIST_ERROR)
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.contact_number = validated_data['contact_number']
        instance.email = validated_data['email']

        instance.save()

        return instance
