# Generated by Django 3.2 on 2021-05-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_ingredient_unique ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='image'),
        ),
    ]
