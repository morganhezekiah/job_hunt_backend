# Generated by Django 4.0.2 on 2022-02-28 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.TextField(default='jsfjf87874mffhf564s494kd', unique=True),
            preserve_default=False,
        ),
    ]
