from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from game_core_api.models import Core, Boost
from game_core_api.serializers import CoreSerializer, BoostSerializer
from django.http import JsonResponse

@login_required()
@api_view(['GET'])
def index(request):
    core, is_created = Core.objects.get_or_create(user=request.user)
    return render(request, 'index.html')
