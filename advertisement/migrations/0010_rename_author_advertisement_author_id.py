# Generated by Django 4.0.6 on 2022-07-26 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0009_alter_advertisement_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='author',
            new_name='author_id',
        ),
    ]
