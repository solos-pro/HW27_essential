# Generated by Django 4.0.6 on 2022-07-25 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('advertisement', '0007_alter_advertisement_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]