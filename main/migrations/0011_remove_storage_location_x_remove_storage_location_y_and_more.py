# Generated by Django 5.1.3 on 2024-12-21 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_category_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='location_x',
        ),
        migrations.RemoveField(
            model_name='storage',
            name='location_y',
        ),
        migrations.AddField(
            model_name='storage',
            name='address',
            field=models.CharField(default='None', max_length=200),
        ),
        migrations.AddField(
            model_name='storage',
            name='name',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='storage',
            name='street',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='bonus',
            field=models.IntegerField(default=0),
        ),
    ]
