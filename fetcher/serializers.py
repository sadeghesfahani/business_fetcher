from rest_framework import serializers
from .models import Business, Activity, Person


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ['id', 'business']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ['id', 'business']


class BusinessSerializer(serializers.ModelSerializer):
    representation = PersonSerializer(many=True, read_only=True)
    activity = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Business
        exclude = ['complete', 'in_process', 'id', 'get_on_next_fetch']
