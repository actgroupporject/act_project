# Generated by Django 5.1.3 on 2024-12-16 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0004_user_company_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("O", "Other")], default="M", max_length=1, verbose_name="성별"
            ),
        ),
    ]