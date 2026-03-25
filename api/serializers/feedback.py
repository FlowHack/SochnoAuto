from rest_framework import serializers

from homepage.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Feedback, который включает информацию о
    пользователе, тексте отзыва и дате создания.
    """

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['avatar_url', 'name_user', 'score', 'feedback', 'answer']

    def get_avatar_url(self, obj):
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return obj.avatar.url
        return None
