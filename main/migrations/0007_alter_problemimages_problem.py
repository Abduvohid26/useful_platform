# Generated by Django 5.0.6 on 2024-07-07 06:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_problems_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemimages',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='main.problems'),
        ),
    ]
