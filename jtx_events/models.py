import datetime

from django.db import models

from rest_framework import serializers


class Event(models.Model):
    """
    An event covered by the JTX, or during which have taken place one or more projections.
    Everything is an event: a standalone projection is an event too. 
    """
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    begin_date = models.DateField(default=datetime.datetime(2015, 1, 1))
    end_date = models.DateField(default=datetime.datetime(2015, 1, 1))
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class EventSerializer(serializers.ModelSerializer):
    from jtx_video.models.projection import Projection
    class Meta:
        model = Event

    projections = serializers.PrimaryKeyRelatedField(many=True, queryset=Projection.objects.all())

    def validate(self, data):
        if data['begin_date'] > data['end_date']:
            raise serializers.ValidationError("end date must occur after begin date")
        return data



