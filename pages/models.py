from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    Big_name = models.CharField(max_length=10, help_text="대분류")
    Small_name = models.CharField(max_length=10, help_text="소분류")

    def __str__(self):
        return f"{self.Big_name} - {self.Small_name}"


class PoleCategory(models.Model):
    POLE_CHOICES = [
        ("영화", "영화"),
        ("드라마", "드라마"),
        ("연극", "연극"),
        ("CF", "CF"),
        ("엔터테이먼트", "엔터테이먼트"),
        ("웹드라마", "웹드라마"),
        ("뮤지컬", "뮤지컬"),
        ("기타", "기타"),
    ]
    name = models.CharField(max_length=10, choices=POLE_CHOICES)

    def __str__(self):
        return self.name


class ActorCategory(models.Model):
    ACTOR_CHOICES = [
        ("주연", "주연"),
        ("조연", "조연"),
        ("단역", "단역"),
        ("아역", "아역"),
        ("단원", "단원"),
        ("엑스트라", "엑스트라"),
        ("기타", "기타"),
    ]
    name = models.CharField(max_length=10, choices=ACTOR_CHOICES)

    def __str__(self):
        return self.name


class HowToCategory(models.Model):
    HOW_TO_CHOICES = [("Email", "Email"), ("Phone", "Phone"), ("양식", "양식")]
    method = models.CharField(max_length=10, choices=HOW_TO_CHOICES)

    def __str__(self):
        return self.method

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("how_to_category_detail", args=[str(self.id)])


class Actor_Info_Category(models.Model):
    ACTOR_INFO_CHOICES1 = [
        ("남자", "남자"),
        ("여자", "여자"),
    ]
    ACTOR_INFO_CHOICES2 = [
        ("10대 이하", "10대 이하"),
        ("10대", "10대"),
        ("20대", "20대"),
        ("30대", "30대"),
        ("40대", "40대"),
        ("50대", "50대"),
        ("60대", "60대"),
        ("60대 이상", "60대 이상"),
    ]
    gender = models.CharField(max_length=10, blank=True, choices=ACTOR_INFO_CHOICES1, default="남자")
    age_range = models.CharField(max_length=10, null=True, blank=True, choices=ACTOR_INFO_CHOICES2)

    def __str__(self):
        return f"{self.gender} - {self.age_range}"


class BookMark(models.Model):
    title = models.CharField("TITLE", max_length=100, blank=True)
    url = models.URLField("URL", unique=True)

    def __str__(self):
        return self.title


class RecruitMain(models.Model):
    work_title = models.CharField(max_length=100, verbose_name="작품명")
    work_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="작품 카테고리")
    deadline = models.DateField(verbose_name="마감일")
    bookmarks = models.ManyToManyField(BookMark, blank=True)
    polecategory = models.ForeignKey(PoleCategory, on_delete=models.CASCADE)
    actorcategory = models.ForeignKey(ActorCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.work_title


class RecruitDetail(models.Model):
    recruitmain = models.OneToOneField(
        RecruitMain,
        on_delete=models.CASCADE,
        related_name="detail",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=100, verbose_name="공고 제목")
    director = models.CharField(max_length=50, verbose_name="감독")
    production = models.CharField(max_length=100, verbose_name="제작사")
    requirements = models.TextField(verbose_name="모집 상세 내용")
    casting_type = models.CharField(max_length=50, verbose_name="모집 유형")
    apply_method = models.ForeignKey(HowToCategory, on_delete=models.CASCADE, verbose_name="지원 방법")

    def get_d_day(self):
        return (self.recruitmain.deadline - timezone.now().date()).days

    class Meta:
        db_table = "casting_detail"


class RecruitImage(models.Model):
    recruit = models.ForeignKey(
        RecruitMain,
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
    recruit = models.ForeignKey(
        RecruitMain,
        on_delete=models.CASCADE,
        related_name="applications",
        null=True,
        blank=True,
        verbose_name="모집 공고",
    )
    height = models.CharField(max_length=10, verbose_name="키")
    weight = models.CharField(max_length=10, verbose_name="몸무게")
    age = models.IntegerField(verbose_name="나이")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "applications"
