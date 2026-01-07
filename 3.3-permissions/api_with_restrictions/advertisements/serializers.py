from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )
        read_only_fields = ['creator', 'created_at']

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context['request'].user
        if not user.is_staff:
            if self.instance is None:
                if data.get('status') == AdvertisementStatusChoices.OPEN:
                    if user.advertisements.filter(status=AdvertisementStatusChoices.OPEN).count() >= 10:
                        raise ValidationError("У Вас не может быть больше 10 открытых объявлений")
            else:
                if 'status' in data and data['status'] == AdvertisementStatusChoices.OPEN:
                    if self.instance.status != AdvertisementStatusChoices.OPEN:
                        if user.advertisements.filter(status=AdvertisementStatusChoices.OPEN).count() >= 10:
                            raise ValidationError("У Вас не может быть больше 10 открытых объявлений")
        return data
