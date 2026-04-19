# from rest_framework import serializers

# class PredictSerializer(serializers.Serializer):
#     file = serializers.ImageField()
# diagnosis/serializers.py
from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    """Sérialiseur pour les prédictions"""
    success = serializers.BooleanField()
    prediction = serializers.CharField()
    confidence = serializers.FloatField()
    is_confident = serializers.BooleanField()
    all_probabilities = serializers.DictField()
    top_3 = serializers.ListField()
    file_name = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=False)

class DiagnosisSerializer(serializers.Serializer):
    """Sérialiseur pour les requêtes de diagnostic"""
    image = serializers.ImageField()