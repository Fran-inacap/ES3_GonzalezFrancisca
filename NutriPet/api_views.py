# NutriPet/api_views.py
from rest_framework import viewsets
from recomendador.models import Registro
from .serializers import RecomendacionSerializer
from .permissions import SoloStaffBorra
from solucion import decidir  # Regla de negocio

class RecomendacionViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.filter(eliminado=False).order_by("-fecha")
    serializer_class = RecomendacionSerializer
    permission_classes = [SoloStaffBorra]

    def _procesar_y_guardar(self, serializer):
        """
        Extrae datos validados, ejecuta la regla de negocio y guarda la instancia.
        Soporta valores parciales o previos en caso de actualización (PATCH/PUT).
        """
        # Si es un update parcial, prioriza validated_data y cae en la instancia actual
        instance = serializer.instance
        especie = serializer.validated_data.get("especie", getattr(instance, "especie", None))
        edad = serializer.validated_data.get("edad", getattr(instance, "edad", None))
        alergeno = serializer.validated_data.get("alergeno", getattr(instance, "alergeno", "")) or "ninguno"

        # Regla de negocio
        resultado = decidir(especie, edad, alergeno)

        serializer.save(resultado=resultado)

    def perform_create(self, serializer):
        self._procesar_y_guardar(serializer)

    def perform_update(self, serializer):
        self._procesar_y_guardar(serializer)