# Generated by Django 4.0.2 on 2022-04-05 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phoneNumber',
            field=models.TextField(),
        ),
    ]
