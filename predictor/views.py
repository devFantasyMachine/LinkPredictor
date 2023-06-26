from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.views.generic import TemplateView

from account.models import User
from predictor.form import AIModelForm
from predictor.models import AIModel, Prediction
from predictor.serializers import AIModelSerializer, PredictionSerializer

import pickle
import tensorflow
from keras.models import load_model
import pandas as pd


cached_models = {}


@login_required(login_url='/login')
def home(request):
    users = User.objects.all()
    ai_models = AIModel.objects.all()

    last_prediction = Prediction.objects.filter()

    if request.user.is_superuser:
        predictions = Prediction.objects.all()
    else:
        predictions = Prediction.objects.filter(user=request.user)

    return render(request, 'welcome/home.html',
                  {'users': users, 'predictions': predictions, 'ai_models': ai_models, 'me': request.user})


@login_required(login_url='/login')
def addModels(request):

    if request.method == 'POST':

        try:
            data = {**request.POST, }
            data.pop("csrfmiddlewaretoken")
            data['precision'] = data['precision'][0]
            data["file"] = request.FILES['file']
            print(data)

            serializer = AIModelSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except Exception:
            pass

    ai_models = AIModel.objects.all()
    models_count = len(ai_models)
    return render(request, 'welcome/models.html', {'ai_models': ai_models, 'models_count': models_count, 'me': request.user})


@login_required(login_url='/login')
def doPredictions(request):

    ai_models = AIModel.objects.all()
    models_count = len(ai_models)

    if request.method == 'POST':

        data = {**request.POST, }
        data.pop("csrfmiddlewaretoken")
        data['ai_model'] = data['ai_model'][0]
        data['date_target'] = data['date_target'][0]
        data["file"] = request.FILES['file']
        data["user"] = request.user
        print(data)

        dataset = pd.read_csv(data["file"], sep=";")
        dataset = dataset.drop(columns=['Unnamed: 4', 'Unnamed: 5', 'Utilization1 [%] - Tx - MAX'])
        print(dataset)
        dataset["date"] = pd.to_datetime(dataset["date"])
        dataset["date"] = pd.to_numeric(dataset["date"])

        minmax_scale_X = pickle.load(open("./models/scaler/minmax_scale_X.pkl", "rb"))
        minmax_scale_y = pickle.load(open("./models/scaler/minmax_scale_y.pkl", "rb"))
        dataset_norm = minmax_scale_X.transform(dataset)
        print(dataset)

        model = AIModel.objects.get(pk=data['ai_model'])
        print(model.file.path)

        if model.file.path in cached_models.keys():
            loaded_model = cached_models[model.file.path]
        else:
            loaded_model = load_model(model.file.path)
            cached_models["{}".format(model.file.path)] = loaded_model

        # pickle.load(open(model.file.path, "rb"))

        predictions = loaded_model.predict(dataset_norm)
        print(predictions)
        user_pred = minmax_scale_y.inverse_transform(predictions)
        print(user_pred)

        serializer = PredictionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return render(request, 'welcome/predictions.html',
                      {'ai_models': ai_models, 'models_count': models_count, "user_pred": user_pred, 'prediction': serializer.data, 'me': request.user})

    return render(request, 'welcome/predictions.html', {'ai_models': ai_models, 'models_count': models_count, 'me': request.user})


@login_required(login_url='/login')
def showusercontent(request):
    users = User.objects.all()
    ai_models = AIModel.objects.all()

    last_prediction = Prediction.objects.filter()

    if request.user.is_superuser:
        predictions = Prediction.objects.all()
    else:
        predictions = Prediction.objects.filter(user=request.user)

    users_count = len(users)
    return render(request, 'welcome/showusercontent.html',
                  {'users': users, 'predictions': predictions, 'users_count': users_count, 'ai_models': ai_models, 'me': request.user})
