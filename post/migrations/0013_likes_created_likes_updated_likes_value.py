# Generated by Django 4.1.5 on 2023-05-03 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_alter_postfilecontent_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='likes',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='likes',
            name='value',
            field=models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default=1, max_length=8),
            preserve_default=False,
        ),
    ]
