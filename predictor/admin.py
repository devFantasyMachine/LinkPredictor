from django.contrib import admin

# Register your models here.
from predictor.models import Prediction, LinkPrediction, LinkEntry

admin.site.register(Prediction)
admin.site.register(LinkPrediction)
admin.site.register(LinkEntry)