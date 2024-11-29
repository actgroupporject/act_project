from django.db import models

# Category




# MainPage
class MainPage(models.Model):
    title = models.CharField(max_length=255)







# Recruit Page
class RecruitDetailedPage(models.Model):
    title = models.CharField(max_length=50, help_text="채용 공고 제목")
    description = models.CharField(max_length=255, help_text="채용 공고 상세 설명")
    description_img = models.ImageField()
    post_at = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()

    class Meta:
        db_table = 'RecruitDetailedPage'