# Generated by Django 4.2.16 on 2024-11-07 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emdcbackend', '0002_remove_scoresheet_fieldtext_scoresheet_field22_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
