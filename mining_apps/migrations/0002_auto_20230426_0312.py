# Generated by Django 3.2.9 on 2023-04-26 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mining_apps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livedoornewscorpus',
            name='id',
        ),
        migrations.AlterField(
            model_name='livedoornewscorpus',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]