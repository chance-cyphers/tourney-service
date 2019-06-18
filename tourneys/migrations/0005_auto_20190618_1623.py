# Generated by Django 2.2.2 on 2019-06-18 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourneys', '0004_auto_20190617_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestant1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contestant1', to='tourneys.RoundContestant')),
                ('contestant2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contestant2', to='tourneys.RoundContestant')),
            ],
        ),
        migrations.AddField(
            model_name='vote',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tourneys.Match'),
        ),
    ]