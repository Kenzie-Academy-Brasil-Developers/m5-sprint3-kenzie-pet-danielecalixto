from rest_framework import serializers

class CharacteristicSerializer(serializers.Serializer):
    name = serializers.CharField()