from rest_framework import serializers

from account.serializers import UserSerializer
from .models import AIModel, Prediction, LinkPrediction, LinkEntry


class AIModelSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize User model.
    """

    class Meta:
        model = AIModel
        fields = '__all__'


class LinkEntrySerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize LinkEntry.
    """

    class Meta:
        model = LinkEntry
        fields = '__all__'


class LinkPredictionSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize Link Prediction.
    """

    link = LinkEntrySerializer()

    class Meta:
        model = LinkPrediction
        fields = '__all__'


class PredictionSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize registration requests and create a new user.
    """

    user = UserSerializer()
    ai_model = AIModelSerializer()
    predictions = LinkPredictionSerializer(many=True)

    class Meta:
        model = Prediction
        fields = '__all__'
