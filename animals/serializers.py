from rest_framework import serializers

from groups.models import Group
from .models import Animal
from characteristics.models import Characteristic

from groups.serializers import GroupSerializer
from characteristics.serializers import CharacteristicSerializer

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer()
    characteristics = CharacteristicSerializer(many=True)

    def create(self, validated_data):
        characteristics_data = validated_data.pop('characteristics')
        group_data = validated_data.pop('group')
        group, created = Group.objects.get_or_create(**group_data)
        group_id = group.id
        animal = Animal.objects.create(group_id=group_id, **validated_data)
        for charac in characteristics_data:
            charac, created = Characteristic.objects.get_or_create(**charac)
            animal.characteristics.add(charac)
        return animal

    def update(self, instance, validated_data):
        non_editable_keys = ("sex", "group")
        for key, value in validated_data.items():
            if key in non_editable_keys:
                raise KeyError
            setattr(instance, key, value)
        instance.save()
        return instance
