# Generated by Django 4.0.6 on 2022-07-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0006_alter_advertisement_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='author',
            field=models.CharField(max_length=20),
        ),
    ]