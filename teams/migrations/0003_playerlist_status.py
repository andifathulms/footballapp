# Generated by Django 4.1.6 on 2023-02-21 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_alter_team_stadium'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerlist',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Permanent'), (2, 'On Loan')], default=1),
        ),
    ]
