# Generated by Django 5.1.3 on 2024-12-10 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookMark",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=100, verbose_name="TITLE")),
                ("url", models.URLField(unique=True, verbose_name="URL")),
            ],
        ),
        migrations.RemoveField(
            model_name="recruitdetail",
            name="deadline",
        ),
        migrations.RemoveField(
            model_name="recruitdetail",
            name="work_category",
        ),
        migrations.RemoveField(
            model_name="recruitdetail",
            name="work_title",
        ),
        migrations.AddField(
            model_name="actor_info_category",
            name="age_range",
            field=models.CharField(
                blank=True,
                choices=[
                    ("10대 이하", "10대 이하"),
                    ("10대", "10대"),
                    ("20대", "20대"),
                    ("30대", "30대"),
                    ("40대", "40대"),
                    ("50대", "50대"),
                    ("60대", "60대"),
                    ("60대 이상", "60대 이상"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="actor_info_category",
            name="gender",
            field=models.CharField(
                blank=True, choices=[("남자", "남자"), ("여자", "여자")], default="남자", max_length=10
            ),
        ),
        migrations.AlterField(
            model_name="recruitdetail",
            name="apply_method",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pages.howtocategory", verbose_name="지원 방법"
            ),
        ),
        migrations.CreateModel(
            name="RecruitMain",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("work_title", models.CharField(max_length=100, verbose_name="작품명")),
                ("deadline", models.DateField(verbose_name="마감일")),
                (
                    "actorcategory",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="pages.actorcategory"),
                ),
                ("bookmarks", models.ManyToManyField(blank=True, to="pages.bookmark")),
                (
                    "polecategory",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="pages.polecategory"),
                ),
                (
                    "work_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pages.category", verbose_name="작품 카테고리"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="application",
            name="recruit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applications",
                to="pages.recruitmain",
                verbose_name="모집 공고",
            ),
        ),
        migrations.AddField(
            model_name="recruitdetail",
            name="recruitmain",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detail",
                to="pages.recruitmain",
            ),
        ),
        migrations.AddField(
            model_name="recruitimage",
            name="recruit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="pages.recruitmain",
            ),
        ),
    ]