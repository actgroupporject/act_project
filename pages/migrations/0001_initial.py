# Generated by Django 5.1.3 on 2024-12-05 07:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Actor_Info_Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
        ),
        migrations.CreateModel(
            name="ActorCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("주연", "주연"),
                            ("조연", "조연"),
                            ("단역", "단역"),
                            ("아역", "아역"),
                            ("단원", "단원"),
                            ("엑스트라", "엑스트라"),
                            ("기타", "기타"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("height", models.CharField(max_length=10, verbose_name="키")),
                ("weight", models.CharField(max_length=10, verbose_name="몸무게")),
                ("age", models.IntegerField(verbose_name="나이")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "applications",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("Big_name", models.CharField(help_text="대분류", max_length=10)),
                ("Small_name", models.CharField(help_text="소분류", max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="HowToCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "method",
                    models.CharField(choices=[("Email", "Email"), ("Phone", "Phone"), ("양식", "양식")], max_length=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PoleCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("영화", "영화"),
                            ("드라마", "드라마"),
                            ("연극", "연극"),
                            ("CF", "CF"),
                            ("엔터테이먼트", "엔터테이먼트"),
                            ("웹드라마", "웹드라마"),
                            ("뮤지컬", "뮤지컬"),
                            ("기타", "기타"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecruitDetail",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100, verbose_name="공고 제목")),
                ("work_category", models.CharField(max_length=50, verbose_name="작품 카테고리")),
                ("work_title", models.CharField(max_length=100, verbose_name="작품명")),
                ("director", models.CharField(max_length=50, verbose_name="감독")),
                ("production", models.CharField(max_length=100, verbose_name="제작사")),
                ("requirements", models.TextField(verbose_name="모집 상세 내용")),
                ("casting_type", models.CharField(max_length=50, verbose_name="모집 유형")),
                ("apply_method", models.CharField(max_length=50, verbose_name="지원 방법")),
                ("deadline", models.DateField(verbose_name="마감일")),
            ],
            options={
                "db_table": "casting_detail",
            },
        ),
        migrations.CreateModel(
            name="RecruitImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "image",
                    models.ImageField(
                        upload_to="casting_images/",
                        validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png"])],
                        verbose_name="공고 이미지",
                    ),
                ),
            ],
        ),
    ]
