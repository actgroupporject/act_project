from django import forms
from .models import RecruitDetailPage

class RecruitDetailPageForm(forms.ModelForm):
    class Meta:
        model = RecruitDetailPage
        fields = ['title', 'description', 'description_img', 'closing_at']
        widgets = {
            'closing_at': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '채용 공고 제목을 입력하세요'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '채용 공고 내용을 입력하세요'
                }
            )
        }