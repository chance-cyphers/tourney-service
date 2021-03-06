# Generated by Django 2.2.2 on 2019-06-17 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourneys', '0003_auto_20190617_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roundcontestant',
            name='votes',
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('round_contestant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='tourneys.RoundContestant')),
            ],
        ),
    ]
