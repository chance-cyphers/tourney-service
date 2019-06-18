# Generated by Django 2.2.2 on 2019-06-17 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourneys', '0002_auto_20190617_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='roundcontestant',
            name='tourney',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='round_contestants', to='tourneys.Tourney'),
        ),
        migrations.AlterField(
            model_name='character',
            name='tourney',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='tourneys.Tourney'),
        ),
    ]