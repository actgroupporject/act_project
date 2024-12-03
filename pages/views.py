from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import ApplicationForm, RecruitDetailForm
from .models import Application, RecruitDetail


class RecruitListView(ListView):
    model = RecruitDetail
    template_name = "recruit/list.html"
    context_object_name = "recruits"

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {}

        category = self.request.GET.get("category")
        pole_category = self.request.GET.get("pole_category")
        actor_category = self.request.GET.get("actor_category")

        if category:
            filters["category"] = category
        if pole_category:
            filters["pole_category"] = pole_category
        if actor_category:
            filters["actor_category"] = actor_category

        return queryset.filter(**filters)


class RecruitDetailView(DetailView):
    model = RecruitDetail
    template_name = "recruit/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["d_day"] = self.object.get_d_day()
        return context


@method_decorator(login_required, name="dispatch")
class RecruitCreateView(CreateView):
    model = RecruitDetail
    form_class = RecruitDetailForm
    template_name = "recruit/form.html"

    def form_valid(self, form):
        recruit = form.save()
        messages.success(self.request, "채용 공고가 저장되었습니다.")
        return redirect("recruit:detail", pk=recruit.pk)


@method_decorator(login_required, name="dispatch")
class RecruitUpdateView(UpdateView):
    model = RecruitDetail
    form_class = RecruitDetailForm
    template_name = "recruit/form.html"


@method_decorator(login_required, name="dispatch")
class RecruitDeleteView(DeleteView):
    model = RecruitDetail
    success_url = reverse_lazy("recruit:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "채용 공고가 삭제되었습니다.")
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class ApplicationView(View):
    @staticmethod
    def apply(request, recruit_id):
        if request.method == "POST":
            form = ApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.save()
                messages.success(request, "지원이 완료되었습니다.")
                return redirect("application_complete")
        else:
            form = ApplicationForm()

        return render(request, "apply_form.html", {"form": form})
