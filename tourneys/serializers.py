from django.contrib.auth.models import User
from rest_framework import serializers

from tourneys.models import Bracket, Tourney, Contestant


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


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ('id', 'name')


class TourneySerializer(serializers.ModelSerializer):
    contestants = ContestantSerializer(many=True)

    class Meta:
        model = Tourney
        fields = ('title', 'contestants')

    def create(self, validated_data):
        contestant_data = validated_data.pop('contestants')
        tourney = Tourney.objects.create(**validated_data)
        for c in contestant_data:
            Contestant.objects.create(tourney=tourney, **c)
        return tourney

