from django import forms
from .models import RecruitDetailedPage


# RecruitDetailedPage closing 사용자 입력받는 From
class RecruitDetailedPageForm(forms.ModelForm):
    class Meta:
        model = RecruitDetailedPage
        fields = ['date']
        widgets = {
            'date': forms.DateInput()
        }