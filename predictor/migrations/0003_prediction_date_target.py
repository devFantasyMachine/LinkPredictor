# Generated by Django 4.2.2 on 2023-06-25 20:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_remove_aimodel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='date_target',
            field=models.DateField(default=datetime.datetime(2023, 6, 25, 20, 36, 54, 400293, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
