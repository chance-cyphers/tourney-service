import io
import json

from datetime import datetime, timezone

from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from tourneys.models import Tourney, Match, Vote, Character
from tourneys.serializers import TourneySerializer, to_tourneys_rep, to_tourney_rep, to_match_rep, \
    to_bracket_rep


@csrf_exempt
def index(request):
    links = {
        "allTourneysLink": "https://tourney-service.herokuapp.com/tourney/v2/tourney"
    }
    return JsonResponse({"links": links, "greeting": "sup"}, safe=False)


@csrf_exempt
def bracket(request, tourney_id):
    if request.method == "GET":
        tourney = Tourney.objects.get(pk=tourney_id)
        update_tourney(tourney)
        return JsonResponse(to_bracket_rep(tourney), safe=False)
    else:
        return HttpResponseNotAllowed("GET")


@csrf_exempt
def tourneys(request):
    if request.method == "GET":
        code = request.GET.get('code')
        if code is None:
            serializer = TourneySerializer(Tourney.objects.all(), many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            tourney = Tourney.objects.get(code=code)
            return JsonResponse(to_tourney_rep(tourney), safe=False)
    if request.method == "POST":
        data = JSONParser().parse(io.BytesIO(request.body))
        serializer = TourneySerializer(data=data)
        serializer.is_valid()
        save = serializer.save()
        return HttpResponse(status=201, content=str(save))
    else:
        return HttpResponseNotAllowed("GET, POST")


@csrf_exempt
def tourneys_v2(request):
    if request.method == "GET":
        return JsonResponse(to_tourneys_rep(Tourney.objects.all()), safe=False)
    else:
        return HttpResponseNotAllowed("GET, POST")


@csrf_exempt
def single_tourney(request, tourney_id):
    if request.method == "GET":
        try:
            return JsonResponse(to_tourney_rep(Tourney.objects.get(pk=tourney_id)), safe=False)
        except Tourney.DoesNotExist:
            raise Http404("Tourney does not exist")
    else:
        return HttpResponseNotAllowed("GET")


@csrf_exempt
def current_match(request, tourney_id):
    if request.method == "GET":
        tourney = Tourney.objects.get(pk=tourney_id)
        update_tourney(tourney)

        match_number = get_current_match_num(tourney)

        if Match.objects.filter(tourney=tourney, sequence=match_number).exists():
            current_match = Match.objects.get(tourney=tourney, sequence=match_number)
            return JsonResponse(to_match_rep(current_match), safe=False)
        else:
            return HttpResponse(status=404)

    else:
        return HttpResponseNotAllowed("GET")


@csrf_exempt
def current_match_v2(request):
    if request.method == "GET":
        code = request.GET.get('code')
        if not Tourney.objects.filter(code=code).exists():
            return HttpResponse(status=404)

        tourney = Tourney.objects.get(code=code)
        update_tourney(tourney)

        match_number = get_current_match_num(tourney)

        if Match.objects.filter(tourney=tourney, sequence=match_number).exists():
            current_match = Match.objects.get(tourney=tourney, sequence=match_number)
            return JsonResponse(to_match_rep(current_match), safe=False)
        else:
            return HttpResponse(status=404)

    else:
        return HttpResponseNotAllowed("GET")


def update_tourney(tourney):
    match_number = get_current_match_num(tourney)

    # update past winners
    past_matches_without_winners = Match.objects.filter(
        tourney=tourney
    ).filter(
        sequence__lt=match_number,
        winner=None
    )
    for m in past_matches_without_winners:
        char1_vote_count = len(m.votes.filter(character=m.character1))
        char2_vote_count = len(m.votes.filter(character=m.character2))
        winner = m.character1 if char1_vote_count >= char2_vote_count else m.character2
        m.winner = winner
        m.save()

    # update match chars
    matches = Match.objects.filter(tourney=tourney)
    for m in matches:
        if m.character1 is None or m.character2 is None:
            m.character1 = m.mom.winner
            m.character2 = m.dad.winner
            m.save()


def get_current_match_num(tourney):
    seconds_elapsed = (datetime.now(timezone.utc) - tourney.start_time).total_seconds()
    return seconds_elapsed // (tourney.match_duration * 60) + 1


@csrf_exempt
def vote(request, match_id, character_id):
    if request.method == "PUT":
        username = request.GET.get('username')
        if username is None:
            return HttpResponse(status=404)

        match = Match.objects.get(pk=match_id)
        character = Character.objects.get(pk=character_id)
        v = Vote.objects.update_or_create(username=username, match=match, defaults={"character": character})
        return HttpResponse(content=str(v))
    else:
        return HttpResponseNotAllowed("PUT")
