from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import RecruitDetailPage
from .forms import RecruitDetailPageForm

class RecruitListView(View):
    def get(self, request):
        recruits = RecruitDetailPage.objects.all().order_by('-post_at')
        return render(request, 'recruit_list.html', {'recruits': recruits})

class RecruitDetailView(View):
    def get(self, request, recruit_id):
        recruit = get_object_or_404(RecruitDetailPage, pk=recruit_id)
        data = {
            'recruit': recruit,
            'd_day': recruit.get_d_day()
        }
        return render(request, 'recruit_detail.html', data)

class RecruitCreateView(View):
    def get(self, request):
        form = RecruitDetailPageForm()
        return render(request, 'recruit_form.html', {'form': form})

    def post(self, request):
        form = RecruitDetailPageForm(request.POST, request.FILES)
        if form.is_valid():
            recruit = form.save()
            return redirect('recruit_detail', recruit_id=recruit.id)
        return render(request, 'recruit_form.html', {'form': form})