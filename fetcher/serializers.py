from rest_framework.serializers import ModelSerializer
from django_celery_beat.models import PeriodicTask

class PeriodicTaskSerializer(ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = "__all__"