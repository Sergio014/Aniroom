# Generated by Django 4.1.3 on 2023-01-20 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_blocked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
    ]
