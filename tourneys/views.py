from django.http import JsonResponse

from tourneys.models import Bracket
from tourneys.serializers import BracketSerializer


def index(request):
    bracket = Bracket(32, "basketball or something")
    serializer = BracketSerializer(bracket)
    return JsonResponse(serializer.data, safe=False)
