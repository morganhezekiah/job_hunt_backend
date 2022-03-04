# Generated by Django 4.0.2 on 2022-03-04 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0003_company_company_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='registerd_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL),
        ),
    ]