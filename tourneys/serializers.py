from django.contrib.auth.models import User
from rest_framework import serializers

from tourneys.models import Tourney, Character, Match
import string
import random

BASE_URL = "https://tourney-service.herokuapp.com"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class CharacterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)


class TourneySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    match_duration = serializers.IntegerField()
    characters = CharacterSerializer(many=True)
    code = serializers.CharField(max_length=10, read_only=True)

    def create(self, validated_data):
        character_data = validated_data.pop('characters')
        match_duration = int(validated_data.pop('match_duration'))
        tourney = Tourney.objects.create(
            match_duration=match_duration,
            code=generate_tourney_code(),
            **validated_data
        )

        for c in character_data:
            Character.objects.create(tourney=tourney, **c)

        characters = Character.objects.filter(tourney=tourney)
        for i in range(0, 8):
            Match.objects.create(
                tourney=tourney,
                sequence=i + 1,
                character1=characters[i * 2],
                character2=characters[i * 2 + 1],
                round=16,
            )

        for i in range(8, 15):
            mom_seq = 15 - (15 - i) * 2
            mom = Match.objects.get(tourney=tourney, sequence=mom_seq)
            dad = Match.objects.get(tourney=tourney, sequence=mom_seq + 1)
            Match.objects.create(
                tourney=tourney,
                sequence=i + 1,
                round=16,
                mom=mom,
                dad=dad,
            )

        return tourney

    def update(self, instance, validated_data):
        pass


def generate_tourney_code():
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(4))


def to_tourneys_rep(tourneys):
    response = []
    for tourney in tourneys:
        response.append(to_tourney_rep(tourney))

    return response


def to_tourney_rep(tourney):
    characters = []
    for c in tourney.characters.all():
        characters.append({
            "id": c.id,
            "name": c.name,
        })
    return {
        "id": tourney.id,
        "title": tourney.title,
        "match_duration": tourney.match_duration,
        "characters": characters,
        "code": tourney.code,
        "links": {
            "self": f"{BASE_URL}/tourney/tourney/{tourney.id}",
            "currentMatch": f"{BASE_URL}/tourney/tourney/{tourney.id}/current-match",
            "bracket": f"{BASE_URL}/tourney/tourney/{tourney.id}/bracket"
        }
    }


def to_match_rep(match):
    return {
        "character1": {
            "name": match.character1.name,
            "voteLink": f"{BASE_URL}/tourney/match/{match.id}/character/{match.character1.id}/vote"
        },
        "character2": {
            "name": match.character2.name,
            "voteLink": f"{BASE_URL}/tourney/match/{match.id}/character/{match.character2.id}/vote"
        }
    }


def to_bracket_rep(tourney):
    r16_characters = [
        {"name": c.name}
        for match in Match.objects.filter(tourney=tourney).filter(sequence__lte=8).order_by("sequence")
        for c in [match.character1, match.character2]
    ]

    r8_matches = Match.objects.filter(tourney=tourney).filter(sequence__gt=8, sequence__lte=12).order_by("sequence")
    r8_characters = []
    for m in r8_matches:
        if m.character1 is not None:
            r8_characters.append({"name": m.character1.name})
        if m.character2 is not None:
            r8_characters.append({"name": m.character2.name})

    semifinals_matches = Match.objects.filter(tourney=tourney).filter(sequence__gt=12, sequence__lte=14).order_by(
        "sequence")
    semifinals_characters = []
    for m in semifinals_matches:
        if m.character1 is not None:
            semifinals_characters.append({"name": m.character1.name})
        if m.character2 is not None:
            semifinals_characters.append({"name": m.character2.name})

    finals_characters = []
    final_match = Match.objects.get(tourney=tourney, sequence=15)
    if final_match.character1 is not None:
        finals_characters.append({"name": final_match.character1.name})
    if final_match.character2 is not None:
        finals_characters.append({"name": final_match.character2.name})

    return {
        "name": tourney.title,
        "code": tourney.code,
        "roundOf16": r16_characters,
        "roundOf8": r8_characters,
        "semifinals": semifinals_characters,
        "finals": finals_characters,
        "winner": None if final_match.winner is None else {"name": final_match.winner.name}
    }
