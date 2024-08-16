from venv import logger

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


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
                  'status', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user = self.context['request'].user
        open_adv_count = Advertisement.objects.filter(creator=user, status=AdvertisementStatusChoices.OPEN).count()

        # Проверяем наличие статуса, если его нет то указываем явно
        status = data.get('status', AdvertisementStatusChoices.OPEN)

        if status == AdvertisementStatusChoices.OPEN and open_adv_count >= 10:
            raise ValidationError("Вы не можете создать более 10 открытых объявлений.")

        return data
