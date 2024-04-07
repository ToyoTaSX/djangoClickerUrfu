from rest_framework.serializers import ModelSerializer
from .models import Boost, Core

class BoostSerializer(ModelSerializer):
    class Meta:
        model = Boost
        fields = "__all__"


class CoreSerializer(ModelSerializer):
    class Meta:
        model = Core
        fields = "__all__"