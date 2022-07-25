# Generated by Django 4.0.6 on 2022-07-25 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='locations',
            field=models.ManyToManyField(null=True, to='users.location'),
        ),
    ]
