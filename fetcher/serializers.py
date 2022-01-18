from rest_framework import serializers
from .models import Business, Activity, Person


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ['id','business','type']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ['id','business']


class BusinessSerializer(serializers.ModelSerializer):
    representation = PersonSerializer(many=True)
    activity = ActivitySerializer(many=True)

    class Meta:
        model = Business
        exclude = ['complete',"other",'in_process','id']
