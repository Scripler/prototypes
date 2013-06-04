from django.forms import ModelForm, Textarea
from models import Epub

class EpubCreateForm(ModelForm):
    class Meta:
        model = Epub
        fields = ('author', 'title', 'text')
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20}),
        }