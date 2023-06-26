from django.urls import path

from .views import home, doPredictions, showusercontent, addModels

app_name = "predictor"

urlpatterns = [

    path('home', home),
    path('showusers', showusercontent),
    path('predictions', doPredictions),
    path('models', addModels),

]
