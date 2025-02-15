# Generated by Django 5.1.3 on 2024-11-27 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_item_calories_item_carbonhydrates_item_fats_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='calories',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='carbonhydrates',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='fats',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='protein',
            field=models.FloatField(default=0),
        ),
    ]
