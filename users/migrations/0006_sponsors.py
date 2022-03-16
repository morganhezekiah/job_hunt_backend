# Generated by Django 4.0.2 on 2022-03-16 07:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userpaymentmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('website', models.TextField()),
                ('joined_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
