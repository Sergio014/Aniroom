# Generated by Django 4.1.3 on 2023-01-21 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_likecomment_answercomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likecomment',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='likecomment',
            name='owner',
        ),
        migrations.DeleteModel(
            name='AnswerComment',
        ),
        migrations.DeleteModel(
            name='LikeComment',
        ),
    ]
