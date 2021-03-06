# Generated by Django 2.2.5 on 2019-09-22 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegrambot', '0004_auto_20190920_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('on_air', models.CharField(max_length=1000, null=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='telegrambot.RadioStation')),
            ],
        ),
    ]
