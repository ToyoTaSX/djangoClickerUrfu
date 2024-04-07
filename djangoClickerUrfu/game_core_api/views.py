from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Boost, Core
from .serializers import BoostSerializer, CoreSerializer
from django.utils.decorators import method_decorator
from django.http import JsonResponse

class BoostViewSet(ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts

    def update(self, request, *args, **kwargs):
        boost = Boost.objects.get(id=kwargs['id'])
        old_stats = BoostSerializer(boost).data
        is_bought = boost.buy()
        new_stats = BoostSerializer(boost).data
        return JsonResponse({"old_stats": old_stats, "new_stats":   new_stats, "is_bought": is_bought})


class ClickView(APIView):
    def get(self, request):
        core = Core.objects.get(user=request.user)
        is_level_up = core.click()
        if is_level_up:
            Boost.objects.create(core=core, price=(core.level - 1) * 100, power=(core.level - 1) * 100,)
        return JsonResponse({'core': CoreSerializer(core).data, 'is_level_up': is_level_up})


class GetCoreView(APIView):
    def get(self, request):
        core = Core.objects.get(user=request.user)
        return JsonResponse({'core': CoreSerializer(core).data})

