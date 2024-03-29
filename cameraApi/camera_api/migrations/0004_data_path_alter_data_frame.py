# Generated by Django 4.0.4 on 2022-05-19 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera_api', '0003_data_name_alter_data_frame'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='path',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='data',
            name='frame',
            field=models.ImageField(upload_to='images/<django.db.models.fields.CharField>'),
        ),
    ]
