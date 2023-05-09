from django import forms
from .models import Data

# class FileForm(forms.ModelForm):
#     class Meta:
#         model = Data
#         fields = ('description', 'document', )

CHOICES = (
    ("1", "Евклидово расстояние"),
    ("2", "Манхэттенское расстояние"),
    ("3", "Евклидово расстояние + частотность"),
    ("4", "Манхэттенское расстояние + частотность"),
    ("5", "Метод опорных векторов"),
)


class UploadFilesForm(forms.Form):
    # files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    pattern = forms.FileField(label="Шаблоны пользователей")
    sessions = forms.FileField(label="Файл с сессиями")
    n_session = forms.IntegerField(label="Номер сессии")
    border = forms.IntegerField(label="Порог")
    choises_field = forms.ChoiceField(choices=CHOICES, label="Метод")
