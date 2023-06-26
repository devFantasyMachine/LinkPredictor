from django.forms import ModelForm
from .models import AIModel


class AIModelForm(ModelForm):
    class Meta:
        model = AIModel
        fields = "__all__"
