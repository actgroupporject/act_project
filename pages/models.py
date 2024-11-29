from sqlite3.dbapi2 import Timestamp

from django.db import models
from django.utils import timezone


# Category




# MainPage
class MainPage(models.Model):
    title = models.CharField(max_length=255)







# Recruit Page

class TimeStampModel(models.Model):
    post_at = models.DateTimeField(auto_now_add=True)
    closing_at = models.DateTimeField()  # auto_now 제거

    class Meta:
        abstract = True

class RecruitDetailPage(TimeStampModel):
    title = models.CharField(max_length=50, help_text="채용 공고 제목")
    description = models.TextField(help_text="채용 공고 상세 설명")
    description_img = models.ImageField(
        upload_to='recruits/',
        blank=True,
        null=True
    )

    def get_d_day(self):
        from django.utils import timezone
        now = timezone.now().date()
        closing_date = self.closing_at.date()
        return (closing_date - now).days

    class Meta:
        db_table = 'recruit_detail_page'  # 스네이크 케이스로 변경