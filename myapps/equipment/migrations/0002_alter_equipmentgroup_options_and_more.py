# Generated by Django 4.1.5 on 2025-07-04 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentgroup',
            options={'verbose_name': 'equipment group', 'verbose_name_plural': 'equipment groups'},
        ),
        migrations.AlterModelOptions(
            name='equipmentitem',
            options={'verbose_name': 'equipment item', 'verbose_name_plural': 'equipment items'},
        ),
    ]
