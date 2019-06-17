from django.contrib.auth.models import User
from rest_framework import serializers

from tourneys.models import Bracket, Tourney, Character, RoundContestant


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class BracketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)
    roundOf16 = serializers.ListField()
    roundOf8 = serializers.ListField()
    semiFinals = serializers.ListField()
    finals = serializers.ListField()
    winner = serializers.ReadOnlyField()

    def create(self, validated_data):
        return Bracket(validated_data.get('id'), validated_data.get('name'))

    def update(self, instance, validated_data):
        pass


class CharacterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)


class TourneySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    characters = CharacterSerializer(many=True)

    def create(self, validated_data):
        character_data = validated_data.pop('characters')
        tourney = Tourney.objects.create(**validated_data)
        for c in character_data:
            new_character = Character.objects.create(tourney=tourney, **c)
            RoundContestant.objects.create(character=new_character, round=16)

        return tourney

    def update(self, instance, validated_data):
        pass
