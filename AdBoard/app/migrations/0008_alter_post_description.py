# Generated by Django 4.2.15 on 2024-09-04 20:49

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_newsletter_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text'),
        ),
    ]
