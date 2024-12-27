from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Category(models.Model):
    BIG_NAME_CHOICES = [
        ("--", "--"),
        ("영화", "영화"),
        ("드라마", "드라마"),
        ("연극", "연극"),
        ("CF", "CF"),
        ("엔터테이먼트", "엔터테이먼트"),
        ("웹드라마", "웹드라마"),
        ("뮤지컬", "뮤지컬"),
        ("기타", "기타"),
    ]
    SMALL_NAME_CHOICES = [
        ("--", "--"),
        ("장편", "장편"),
        ("단편", "단편"),
        ("CF", "CF"),
        ("기타", "기타"),
    ]

    big_name = models.CharField(max_length=20, choices=BIG_NAME_CHOICES, default=1)
    small_name = models.CharField(max_length=20, choices=SMALL_NAME_CHOICES, default=1)

    def __str__(self):
        return f"{self.small_name} - {self.big_name}"


class ActorCategory(models.Model):
    ACTOR_CHOICES = [
        ("--", "--"),
        ("주연", "주연"),
        ("조연", "조연"),
        ("단역", "단역"),
        ("아역", "아역"),
        ("단원", "단원"),
        ("엑스트라", "엑스트라"),
        ("기타", "기타"),
    ]
    name = models.CharField(max_length=10, choices=ACTOR_CHOICES, default=1)

    def __str__(self):
        return self.name


class HowToCategory(models.Model):
    HOW_TO_CHOICES = [("--", "--"), ("Email", "Email"), ("Phone", "Phone"), ("양식", "양식")]
    method = models.CharField(max_length=10, choices=HOW_TO_CHOICES, default=1)

    def __str__(self):
        return self.method

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("how_to_category_detail", args=[str(self.id)])


class Gender(models.Model):
    GENDER_CHOICES = [
        ("남자", "남자"),
        ("여자", "여자"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=1)

    def __str__(self):
        return self.gender


class AgeRange(models.Model):
    AGE_RANGE_CHOICES = [
        ("10대 이하", "10대 이하"),
        ("10대", "10대"),
        ("20대", "20대"),
        ("30대", "30대"),
        ("40대", "40대"),
        ("50대", "50대"),
        ("60대", "60대"),
        ("60대 이상", "60대 이상"),
    ]
    age_range = models.CharField(max_length=10, choices=AGE_RANGE_CHOICES, default=1)

    def __str__(self):
        return self.age_range


class Education(models.Model):
    EDUCATION_CHOICES = [
        ("초등학교", "초등학교"),
        ("중학교", "중학교"),
        ("고등학교", "고등학교"),
        ("대학교", "대학교"),
        ("기타", "기타"),
    ]
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default=1)

    def __str__(self):
        return self.education


class BookMark(models.Model):
    title = models.CharField("TITLE", max_length=100, blank=True)
    url = models.URLField("URL", unique=True)

    def __str__(self):
        return self.title


# 공고
class Recruit(models.Model):
    title = models.CharField("TITLE", max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, help_text="작품 카테고리")
    post_at = models.DateField(help_text="공고 등록일")
    closing_at = models.DateField(help_text="공고 마감일")
    bookmark = models.ManyToManyField(BookMark, blank=True)
    progress = models.BooleanField(default=False, help_text="진행상황")
    movie_title = models.CharField("TITLE", max_length=100, blank=True)
    director = models.CharField(max_length=50, verbose_name="감독")
    production = models.CharField(max_length=100, verbose_name="제작사")
    requirements = models.TextField(verbose_name="모집 상세 내용")
    casting_type = models.CharField(max_length=50, verbose_name="모집 유형")
    apply_method = models.ForeignKey(HowToCategory, on_delete=models.CASCADE, verbose_name="지원 방법")

    # 유저의 정보가 user인지 company인지 확인
    @classmethod
    def create_recruit(cls, user):
        if not user.is_company():  # 유저의 정보가 company가 아니라면
            raise ValueError("기업 회원만 공고를 생성할 수 있습니다.")
        return cls.objects.create()  # 유저의 정보가 company가 맞다면 공고 생성

    class Meta:
        db_table = "recruit"
        verbose_name = "공고"
        verbose_name_plural = "공고들"

    def __str__(self):
        return self.title


class RecruitImage(models.Model):
    recruit = models.ForeignKey(
        Recruit,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="casting_images/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
        verbose_name="공고 이미지",
    )


class Application(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, null=False, default=1)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, verbose_name="성별", default=1)
    height = models.CharField(max_length=10, verbose_name="키")
    weight = models.CharField(max_length=10, verbose_name="몸무게")
    age_range = models.ForeignKey(AgeRange, on_delete=models.CASCADE, verbose_name="나이", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "applications"

    def __str__(self):
        return f"{self.actor} applied to {self.recruit}"



class Actor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_info = models.CharField(max_length=255, blank=True, help_text="배우 소개")
    stature = models.IntegerField()
    weight = models.FloatField()
    education = models.ForeignKey(Education, on_delete=models.SET_NULL, null=True, blank=True)
    specialty = models.CharField(max_length=255, blank=True)
    agency = models.CharField(max_length=255, blank=True)
    sns = models.CharField(max_length=255, blank=True)
    bookmark = models.ManyToManyField(BookMark, blank=True)

    def __str__(self):
        return self.user.username


class ActorImage(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="Actor_images/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
        verbose_name="배우 이미지",
    )


class ActorVideo(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        related_name="videos",
        null=True,
        blank=True,
    )
    video = models.FileField(
        upload_to="Actor_videos/",
        validators=[FileExtensionValidator(["mp4", "avi", "mov"])],
        verbose_name="배우 동영상",
    )
    title = models.CharField(max_length=100, blank=True, help_text="동영상 제목")
    description = models.TextField(blank=True, help_text="동영상 설명")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor.user.username} - {self.title}"
