# Generated by Django 5.0.3 on 2024-04-06 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonthlyCategory', '0002_monthlycategory_month_monthlycategory_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlycategory',
            name='month_year',
        ),
        migrations.AlterField(
            model_name='monthlycategory',
            name='month',
            field=models.IntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='monthlycategory',
            name='year',
            field=models.IntegerField(default=2024),
        ),
    ]
