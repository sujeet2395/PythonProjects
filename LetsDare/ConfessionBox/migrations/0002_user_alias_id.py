# Generated by Django 3.0.2 on 2020-07-16 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConfessionBox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='alias_id',
            field=models.CharField(default='defaul', max_length=10, unique=True),
        ),
    ]
