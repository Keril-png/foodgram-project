# Generated by Django 3.2 on 2021-04-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20210424_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='value',
            field=models.PositiveIntegerField(null=True, verbose_name='value'),
        ),
    ]
