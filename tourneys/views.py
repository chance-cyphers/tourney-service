import io

from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from tourneys.models import Bracket, Tourney, Vote, RoundContestant, Match
from tourneys.serializers import BracketSerializer, TourneySerializer


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
def tourney(request):
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
def single_tourney(request, tourney_id):
    if request.method == "GET":
        try:
            serializer = TourneySerializer(Tourney.objects.get(pk=tourney_id))
            return JsonResponse(serializer.data, safe=False)
        except Tourney.DoesNotExist:
            raise Http404("Tourney does not exist")
    else:
        return HttpResponseNotAllowed("GET")


@csrf_exempt
def current_match(request, tourney_id):
    if request.method == "GET":
        return JsonResponse(tourney_id, safe=False)
    else:
        return HttpResponseNotAllowed("GET")


@csrf_exempt
def vote(request, match_id, rc_id, username):
    if request.method == "PUT":
        rc = RoundContestant.objects.get(pk=rc_id)
        match = Match.objects.get(pk=match_id)
        v = Vote.objects.update_or_create(username=username, match=match, defaults={"round_contestant": rc})
        return HttpResponse(content=str(v))
    else:
        return HttpResponseNotAllowed("PUT")
