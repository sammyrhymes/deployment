# Generated by Django 5.0.7 on 2024-08-26 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_mpesatransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cars/')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='competition.competition')),
            ],
        ),
    ]
