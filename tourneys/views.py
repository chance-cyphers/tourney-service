import io

from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from tourneys.models import Bracket, Tourney
from tourneys.serializers import BracketSerializer, TourneySerializer, TourneySerializerV2


@csrf_exempt
def example_bracket(request):
    bracket = Bracket(32, "Board Games")
    serializer = BracketSerializer(bracket)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def index(request):
    links = {
        "currentBracketLink": "https://tourney-service.herokuapp.com/tourney/bracket/example",
    }
    return JsonResponse({"links": links, "greeting": "sup"}, safe=False)


@csrf_exempt
def tourneys(request):
    if request.method == "GET":
        serializer = TourneySerializer(Tourney.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        data = JSONParser().parse(io.BytesIO(request.body))
        serializer = TourneySerializer(data=data)
        serializer.is_valid()
        serializer.save()
        return HttpResponse(status=201)
    else:
        return HttpResponseNotAllowed("GET, POST")


@csrf_exempt
def tourney_v2(request):
    if request.method == "POST":
        data = JSONParser().parse(io.BytesIO(request.body))
        serializer = TourneySerializerV2(data=data)
        serializer.is_valid()
        serializer.save()
        return HttpResponse(status=201)
    else:
        return HttpResponseNotAllowed("POST")


@csrf_exempt
def single_tourney(request, tourney_id):
    if request.method == "GET":
        try:
            serializer = TourneySerializer(Tourney.objects.get(pk=tourney_id))
            return JsonResponse(serializer.data, safe=False)
        except Tourney.DoesNotExist:
            raise Http404("Tourney does not exist")
    else:
        return HttpResponseNotAllowed("GET")
