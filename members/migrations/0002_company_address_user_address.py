# Generated by Django 5.1.3 on 2024-12-10 08:23

from django.db import migrations, models

import members.validators


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="address",
            field=models.CharField(
                default="Unknown",
                max_length=255,
                null=True,
                validators=[members.validators.validate_kakao_address],  # type: ignore
                verbose_name="회사 주소",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.CharField(
                default="Unknown",
                max_length=255,
                validators=[members.validators.validate_kakao_address],  # type: ignore
                verbose_name="유저 주소",
            ),
        ),
    ]
