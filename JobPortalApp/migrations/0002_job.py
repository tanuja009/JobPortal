# Generated by Django 5.0.6 on 2024-10-08 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobPortalApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
