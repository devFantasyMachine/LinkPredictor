from django.db import models
from django.utils import timezone

from account.models import User


def upload_to(instance, filename):
    return "models/{}".format(timezone.now())


class LinkEntry(models.Model):
    """

    """
    name = models.TextField(blank=False)
    code = models.CharField(max_length=100)
    bandwidth = models.FloatField(blank=False)
    rate = models.FloatField(blank=False)
    date = models.DateTimeField(blank=False)
    usage = models.FloatField(blank=False)


class AIModel(models.Model):
    """

    """
    file = models.FileField(blank=False, upload_to=upload_to)
    usage_count = models.IntegerField(blank=False, default=0)
    added_at = models.DateTimeField(blank=False, auto_now_add=True)
    precision = models.FloatField(blank=False)


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    compute_at = models.DateTimeField(blank=False, auto_now_add=True)
    date_target = models.DateField(blank=False)
    # file = models.FileField(blank=False, upload_to=upload_to)


class LinkPrediction(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    link = models.ForeignKey(LinkEntry, on_delete=models.CASCADE)

