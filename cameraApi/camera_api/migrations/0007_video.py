# Generated by Django 4.0.4 on 2022-08-02 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera_api', '0006_alter_data_frame'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('time_interval', models.CharField(max_length=100)),
            ],
        ),
    ]
