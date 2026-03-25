from rest_framework import serializers

from homepage.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Feedback, который включает информацию о
    пользователе, тексте отзыва и дате создания.
    """

    avatar_url = serializers.CharField(source='avatar.url', allow_null=True)

    class Meta:
        model = Feedback
        fields = ['avatar_url', 'name_user', 'score', 'feedback', 'answer']
