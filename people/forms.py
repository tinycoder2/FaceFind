
from django import forms

from people.models import MissingPerson, ReportedPerson

class MissingPersonCreateForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = MissingPerson
        # fields = "__all__"
        exclude = ['status', 'is_verified', 'face_id']


class MissingPersonUpdateForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = MissingPerson
        exclude = ['face_id', 'is_verified']
        # fields = "__all__"
        

class MissingPersonVerifyForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = MissingPerson
        # exclude = ['face_id']
        fields = ['is_verified']



class ReportedPersonCreateForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = ReportedPerson
        # fields = "__all__"
        exclude = ['is_verified', 'face_id']


class ReportedPersonUpdateForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = ReportedPerson
        exclude = ['face_id']
        # fields = "__all__"
        

class ReportedPersonVerifyForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = ReportedPerson
        # exclude = ['face_id']
        fields = ['is_verified']