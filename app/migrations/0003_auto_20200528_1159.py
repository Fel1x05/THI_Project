# Generated by Django 3.0.5 on 2020-05-28 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200528_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='result_time',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='time',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
