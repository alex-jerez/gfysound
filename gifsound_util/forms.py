from django.forms import ModelForm
from .models import Gifsound


class GifsoundForm(ModelForm):
    class Meta:
        model = Gifsound
