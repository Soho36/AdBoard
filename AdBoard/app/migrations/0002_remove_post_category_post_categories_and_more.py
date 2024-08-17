# Generated by Django 4.2.15 on 2024-08-17 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='posts', to='app.category'),
        ),
        migrations.DeleteModel(
            name='PostCategory',
        ),
    ]
