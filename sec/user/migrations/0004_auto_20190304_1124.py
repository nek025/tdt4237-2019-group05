# Generated by Django 2.1.7 on 2019-03-04 11:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190209_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='security_question',
            field=models.TextField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='security_question_answer',
            field=models.TextField(default='', max_length=254),
            preserve_default=False,
        ),
    ]