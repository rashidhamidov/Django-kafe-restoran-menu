# Generated by Django 3.0.7 on 2020-08-16 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='categori',
            name='tip',
            field=models.CharField(blank=True, choices=[('Menu', 'Menu'), ('categori', 'categori')], max_length=10),
        ),
        migrations.AddField(
            model_name='urun',
            name='tip',
            field=models.CharField(blank=True, choices=[('Menu', 'Menu'), ('Haber', 'Haber'), ('Etkinlik', 'Etkinlik'), ('Duyuru', 'Duyuru')], max_length=10),
        ),
    ]
