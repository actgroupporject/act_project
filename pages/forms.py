from django import forms
from django.utils import timezone
from .models import RecruitDetail, PoleCategory, ActorCategory, Application

class RecruitDetailForm(forms.ModelForm):
    class Meta:
        model = RecruitDetail
        fields = [
            "title",
            "pole_category",
            "actor_category",
            "work_category",
            "title_name",
            "direction_name",
            "description",
            "description_img",
            "refer_to",
            "how_apply",
            "shoot_at",
            "post_at",
            "closing_at"
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "공고 제목을 입력하세요"
            }),
            "title_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "작품명을 입력하세요"
            }),
            "direction_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "감독명을 입력하세요"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "상세 내용을 입력하세요",
                "rows": 5
            }),
            "refer_to": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "참고사항을 입력하세요",
                "rows": 3
            }),
            "description_img": forms.FileInput(attrs={
                "class": "form-control-file"
            }),
            "closing_at": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control"
            }),
            "shoot_at": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        closing_at = cleaned_data.get('closing_at')
        shoot_at = cleaned_data.get('shoot_at')

        if closing_at and closing_at < timezone.now():
            raise forms.ValidationError("마감일은 현재 시간 이후여야 합니다.")

        if shoot_at and shoot_at < timezone.now().date():
            raise forms.ValidationError("촬영 일정은 현재 날짜 이후여야 합니다.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pole_category'].widget.attrs.update({'class': 'form-control'})
        self.fields['actor_category'].widget.attrs.update({'class': 'form-control'})
        self.fields['work_category'].widget.attrs.update({'class': 'form-control'})
        self.fields['how_apply'].widget.attrs.update({'class': 'form-control'})

class ApplicationForm(forms.ModelForm):
    class Meta:
        fields = [
            "apply_role_title",
            "apply_role",
            "actor_info_category",
            "apply_role_description",
        ]