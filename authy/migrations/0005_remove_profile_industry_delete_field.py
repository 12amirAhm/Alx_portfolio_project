# Generated by Django 4.1.7 on 2023-02-19 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0004_field_profile_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Industry',
        ),
        migrations.DeleteModel(
            name='Field',
        ),
    ]
