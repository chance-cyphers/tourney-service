from django.contrib.auth.models import User
from rest_framework import serializers

from tourneys.models import Bracket


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class BracketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)
    roundOf16 = serializers.ListField()

    def create(self, validated_data):
        return Bracket(validated_data.get('id'), validated_data.get('name'))

    def update(self, instance, validated_data):
        pass
