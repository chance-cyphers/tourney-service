import io
import json

from datetime import datetime, timezone

from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from tourneys.models import Bracket, Tourney, Match, Vote, Character
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
def tourneys(request):
    if request.method == "GET":
        serializer = TourneySerializer(Tourney.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        data = JSONParser().parse(io.BytesIO(request.body))
        serializer = TourneySerializer(data=data)
        serializer.is_valid()
        save = serializer.save()
        return HttpResponse(status=201, content=str(save))
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
        # find tourney
        tourney = Tourney.objects.get(pk=tourney_id)

        # calc match seq # by tourney time
        seconds_elapsed = (datetime.now(timezone.utc) - tourney.start_time).total_seconds()
        match_number = seconds_elapsed // (tourney.match_duration * 60) + 1

        # get all matches <= seq
        past_matches = Match.objects.filter(
            tourney=tourney
        ).filter(
            sequence__lt=match_number
        )

        # update winners if null
        for m in past_matches:
            if m.winner is None:
                print('match: ' + str(m.sequence))
                char1_votes = m.votes.filter(character=m.character1)
                char2_votes = m.votes.filter(character=m.character2)
                print(len(char1_votes))
                print(len(char2_votes))

        # update current match chars if needed

        return JsonResponse("matches: " + str(match_number), safe=False)
    else:
        return HttpResponseNotAllowed("GET")


@csrf_exempt
def vote(request, match_id, character_id, username):
    if request.method == "PUT":
        # data = JSONParser().parse(io.BytesIO(request.body))
        match = Match.objects.get(pk=match_id)
        character = Character.objects.get(pk=character_id)
        v = Vote.objects.update_or_create(username=username, match=match, defaults={"character": character})
        return HttpResponse(content=str(v))
    else:
        return HttpResponseNotAllowed("PUT")
