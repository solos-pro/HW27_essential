# Generated by Django 4.0.6 on 2022-07-26 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0010_rename_author_advertisement_author_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='author_id',
            new_name='author',
        ),
    ]
