# Generated by Django 4.1.7 on 2023-03-18 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_remove_post_videopic_alter_post_postpic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfilecontent',
            name='file',
            field=models.FileField(upload_to='video/%y'),
        ),
    ]
