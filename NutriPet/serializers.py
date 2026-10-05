# NutriPet/serializers.py
from rest_framework import serializers
from recomendador.models import Registro

class RecomendacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ['id', 'nombre', 'especie', 'edad', 'alergeno', 'resultado', 'fecha']
        read_only_fields = ['resultado', 'fecha']

    def validate_edad(self, valor):
        if valor < 0:
            raise serializers.ValidationError("La edad de la mascota no puede ser negativa.")
        return valor