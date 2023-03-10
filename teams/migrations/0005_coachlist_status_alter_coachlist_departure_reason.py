# Generated by Django 4.1.6 on 2023-03-05 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_alter_playerlist_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachlist',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager'), (2, 'Caretaker')], default=1),
        ),
        migrations.AlterField(
            model_name='coachlist',
            name='departure_reason',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Sacked'), (2, 'Mutual Consent'), (3, 'Resigned'), (4, 'End of Caretaker Spell')], null=True),
        ),
    ]
