# Generated by Django 4.2rc1 on 2025-01-12 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0003_alter_requestresponse_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestresponse',
            name='request',
            field=models.JSONField(default=None),
        ),
        migrations.AlterField(
            model_name='requestresponse',
            name='response',
            field=models.JSONField(default=None),
        ),
    ]
