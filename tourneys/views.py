from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tourneys.models import Bracket
from tourneys.serializers import BracketSerializer


@csrf_exempt
def index(request):
    bracket = Bracket(32, "Board Games")
    serializer = BracketSerializer(bracket)
    return JsonResponse(serializer.data, safe=False)
