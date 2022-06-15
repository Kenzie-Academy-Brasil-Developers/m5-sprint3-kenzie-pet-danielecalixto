from rest_framework import serializers
from groups.serializers import GroupSerializer
from groups.models import Group
from characteristics.serializers import CharacteristicSerializer
from characteristics.models import Characteristic
from .models import Animal
# from animals.serializers import AnimalSerializer
# serializer = AnimalSerializer(data=animal_data)
class AnimalSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer()
    characteristics = CharacteristicSerializer(many=True)

    def create(self, validated_data):
        print(validated_data)
        characteristics_data = validated_data.pop('characteristics')
        group_data = validated_data.pop('group')
        group = Group.objects.create(**group_data)
        group_id = group.id
        characteristics_list = list()
        for charac in characteristics_data:
            characteristic = Characteristic.objects.create(**charac)
            characteristics_list.append(characteristic.id)
        animal = Animal.objects.create(group_id=group_id, characteristics=characteristics_list, **validated_data)
        return animal