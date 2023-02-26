# Generated by Django 4.1.6 on 2023-02-26 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_remove_player_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='preferred_foot',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Left'), (2, 'Right'), (3, 'Both')], null=True),
        ),
        migrations.CreateModel(
            name='MarketValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('last_update_value', models.DateField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='market_values', to='players.player')),
            ],
        ),
    ]
