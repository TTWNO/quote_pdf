# Generated by Django 3.1.2 on 2020-11-07 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0010_downloadattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='downloadattempt',
            name='geolocation',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
