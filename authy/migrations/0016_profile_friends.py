# Generated by Django 4.1.7 on 2023-03-10 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0015_friend_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(related_name='my_friends', to='authy.friend'),
        ),
    ]
