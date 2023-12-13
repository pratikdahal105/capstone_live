# Generated by Django 4.2.5 on 2023-10-06 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='sponsors/logos/')),
                ('description', models.TextField()),
                ('amount_sponsored', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sponsor_level', models.PositiveSmallIntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
            options={
                'db_table': 'sponsor',
            },
        ),
    ]