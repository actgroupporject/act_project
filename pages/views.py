from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Application, BookMark, RecruitDetail, RecruitMain


class RecruitMainListView(ListView):
    model = RecruitMain
    template_name = "recruit_main_list.html"
    context_object_name = "recruits"


class RecruitMainDetailView(DetailView):
    model = RecruitMain
    template_name = "recruit_main_detail.html"
    context_object_name = "recruit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail"] = self.object.recruitdetail
        context["images"] = self.object.images.all()
        return context


class RecruitMainCreateView(CreateView):
    model = RecruitMain
    template_name = "recruit_main_form.html"
    fields = ["work_title", "work_category", "deadline", "polecategory", "actorcategory"]
    success_url = reverse_lazy("recruit_main_list")


class RecruitMainUpdateView(UpdateView):
    model = RecruitMain
    template_name = "recruit_main_form.html"
    fields = ["work_title", "work_category", "deadline", "polecategory", "actorcategory"]
    success_url = reverse_lazy("recruit_main_list")


class RecruitMainDeleteView(DeleteView):
    model = RecruitMain
    template_name = "recruit_main_confirm_delete.html"
    success_url = reverse_lazy("recruit_main_list")


class BookMarkListView(ListView):
    model = BookMark
    template_name = "bookmark_list.html"
    context_object_name = "bookmarks"


class BookMarkCreateView(CreateView):
    model = BookMark
    template_name = "bookmark_form.html"
    fields = ["title", "url"]
    success_url = reverse_lazy("bookmark_list")


def add_bookmark(request, pk):
    recruit = get_object_or_404(RecruitMain, pk=pk)
    bookmark, created = BookMark.objects.get_or_create(
        title=recruit.work_title, url=request.build_absolute_uri(recruit.get_absolute_url())
    )
    recruit.bookmarks.add(bookmark)
    return redirect("recruit_main_detail", pk=pk)


class ApplicationCreateView(CreateView):
    model = Application
    template_name = "application_form.html"
    fields = ["height", "weight", "age"]

    def form_valid(self, form):
        form.instance.recruit = get_object_or_404(RecruitMain, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recruit_main_detail", kwargs={"pk": self.kwargs["pk"]})
