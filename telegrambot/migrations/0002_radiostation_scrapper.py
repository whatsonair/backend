# Generated by Django 2.1.1 on 2019-08-22 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegrambot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadioStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('monitor', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('python_path', models.CharField(max_length=1000)),
                ('priority', models.IntegerField(unique=True)),
                ('used', models.IntegerField(default=0)),
                ('success', models.IntegerField(default=0)),
                ('radio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegrambot.RadioStation')),
            ],
        ),
    ]
