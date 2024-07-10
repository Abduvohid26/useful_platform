# Generated by Django 5.0.6 on 2024-07-10 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_questionresult_is_correct'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(default='logo.jpg', upload_to='site-logo')),
                ('facebook', models.CharField(max_length=255)),
                ('twitter', models.CharField(max_length=255)),
                ('linkedin', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
    ]
