# Generated by Django 3.2.3 on 2021-05-19 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210517_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='visibility',
            field=models.CharField(choices=[('P', 'Private'), ('F', 'Friends'), ('E', 'Everyone')], default='P', max_length=1),
        ),
    ]