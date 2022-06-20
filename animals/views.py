from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from .models import Animal
from .serializers import AnimalSerializer

class AnimalView(APIView):
    def get(self, _):
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data)    

    def post(self, request):
        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)    

class AnimalViewDetail(APIView):
    def get(self, request, animal_id):
        try:
            animal = Animal.objects.get(pk=animal_id)
        except Animal.DoesNotExist:
            return Response({"message": "Animal not found"}, status.HTTP_404_NOT_FOUND)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)
    
    def delete(self, request, animal_id):
        animal = get_object_or_404(Animal, pk=animal_id)
        animal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, animal_id):
        animal = get_object_or_404(Animal, pk=animal_id)
        serializer = AnimalSerializer(animal, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except KeyError as err:
            return Response(
                {"error": f'You can not update {err.args[0]} property'}, status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data)