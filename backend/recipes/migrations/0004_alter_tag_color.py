# Generated by Django 3.2.13 on 2022-05-24 20:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220524_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator(message='Цвет должен быть в HEX кодировке.', regex='#[A-Fa-f\\d]{6}')], verbose_name='Цвет в HEX'),
        ),
    ]
