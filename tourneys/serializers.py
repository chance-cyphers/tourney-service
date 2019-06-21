from django.contrib.auth.models import User
from rest_framework import serializers

from tourneys.models import Bracket, Tourney, Character, Match


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
        tourney = Tourney.objects.create(match_duration=1, **validated_data)

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
