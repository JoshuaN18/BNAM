# Generated by Django 5.0.3 on 2024-03-15 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_alter_account_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('Savings', 'Savings'), ('Checking', 'Checking'), ('Investment', 'Investment'), ('Credit', 'Credit')], default='Checking', max_length=50),
        ),
    ]
