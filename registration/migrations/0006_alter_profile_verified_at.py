# Generated by Django 4.2.6 on 2023-10-13 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_alter_profile_phone_alter_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='verified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
