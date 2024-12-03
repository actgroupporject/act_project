from django import forms
from django.utils import timezone

from .models import ActorCategory, Application, PoleCategory, RecruitDetail


class RecruitDetailForm(forms.ModelForm):
    class Meta:
        model = RecruitDetail
        fields = [
            "work_category",
            "work_title",
            "director",
            "production",
            "requirements",
            "casting_type",
            "apply_method",
            "deadline",
        ]

        widgets = {
            "work_title": forms.TextInput(attrs={"class": "form-control", "placeholder": "작품명을 입력하세요"}),
            "director": forms.TextInput(attrs={"class": "form-control", "placeholder": "감독명을 입력하세요"}),
            "production": forms.TextInput(attrs={"class": "form-control", "placeholder": "제작사를 입력하세요"}),
            "requirements": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "모집 상세 내용을 입력하세요", "rows": 5}
            ),
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data.get("deadline")

        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("촬영 일정은 현재 날짜 이후여야 합니다.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["work_category"].widget.attrs.update({"class": "form-control"})
        self.fields["casting_type"].widget.attrs.update({"class": "form-control"})
        self.fields["apply_method"].widget.attrs.update({"class": "form-control"})


class ApplicationForm(forms.ModelForm):
    class Meta:
        fields = [
            "apply_role_title",
            "apply_role",
            "actor_info_category",
            "apply_role_description",
        ]
