# Generated by Django 4.1.7 on 2023-02-26 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import post.models
import post.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0010_post_videopic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='videopic',
        ),
        migrations.AlterField(
            model_name='post',
            name='postpic',
            field=models.ImageField(null=True, upload_to=post.models.user_directory_path, verbose_name='Postpic'),
        ),
        migrations.CreateModel(
            name='PostFileContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='video/%y', validators=[post.validators.file_size])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.ManyToManyField(related_name='contents', to='post.postfilecontent'),
        ),
    ]
