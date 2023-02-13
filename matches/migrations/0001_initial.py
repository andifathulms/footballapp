# Generated by Django 4.1.6 on 2023-02-13 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("regions", "0001_initial"),
        ("stadiums", "0001_initial"),
        ("teams", "0001_initial"),
        ("coaches", "0001_initial"),
        ("competitions", "0001_initial"),
        ("players", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Formation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="LineUp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Home"), (2, "Away")]
                    ),
                ),
                (
                    "coach",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_lineups",
                        to="coaches.coach",
                    ),
                ),
                (
                    "formation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_lineups",
                        to="matches.formation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("home_score", models.PositiveSmallIntegerField(default=0)),
                ("away_score", models.PositiveSmallIntegerField(default=0)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Not Started"),
                            (2, "Half Time"),
                            (3, "Full Time"),
                            (9, "Postponed"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "away_team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="away_matches",
                        to="teams.team",
                    ),
                ),
                (
                    "competition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="matches",
                        to="competitions.competition",
                    ),
                ),
                (
                    "home_team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="home_matches",
                        to="teams.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MatchCards",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "half",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "First Half"),
                            (2, "Second Half"),
                            (3, "Extra Time First Half"),
                            (4, "Extra Time Second Half"),
                        ]
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Yellow"), (2, "Yellow"), (3, "Red")]
                    ),
                ),
                ("minute", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Substitution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "half",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "First Half"),
                            (2, "Second Half"),
                            (3, "Extra Time First Half"),
                            (4, "Extra Time Second Half"),
                        ]
                    ),
                ),
                ("minute", models.PositiveIntegerField()),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="substitutions",
                        to="matches.match",
                    ),
                ),
                (
                    "player_in",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="in_substitutions",
                        to="players.player",
                    ),
                ),
                (
                    "player_out",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="out_substitutions",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Referee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "nationality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referees",
                        to="regions.country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayerRole",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_captain", models.BooleanField(default=False)),
                (
                    "lineup",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="matches.lineup"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="players.player"
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="players.position",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MissedPenalty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Saved"), (2, "Missed"), (3, "Hit the Crossbar")]
                    ),
                ),
                (
                    "half",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "First Half"),
                            (2, "Second Half"),
                            (3, "Extra Time First Half"),
                            (4, "Extra Time Second Half"),
                            (5, "Penalty Shoot-Out"),
                        ]
                    ),
                ),
                ("minute", models.PositiveIntegerField()),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="missed_penalties",
                        to="matches.match",
                    ),
                ),
                (
                    "penalty_taker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="missed_penalties",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MatchOfficial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_additional_referee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="first_additional_officials",
                        to="matches.referee",
                    ),
                ),
                (
                    "first_assistant_referee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="first_assistant_officials",
                        to="matches.referee",
                    ),
                ),
                (
                    "match",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_officials",
                        to="matches.match",
                    ),
                ),
                (
                    "referee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="main_officials",
                        to="matches.referee",
                    ),
                ),
                (
                    "reserve_referee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reserve_officials",
                        to="matches.referee",
                    ),
                ),
                (
                    "second_additional_referee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="second_additional_officials",
                        to="matches.referee",
                    ),
                ),
                (
                    "second_assistant_referee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="second_assistant_officials",
                        to="matches.referee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MatchData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("kick_off_time", models.DateTimeField()),
                ("attendance", models.IntegerField()),
                ("first_half_added_time", models.PositiveSmallIntegerField()),
                ("second_half_added_time", models.PositiveSmallIntegerField()),
                (
                    "et_first_half_added_time",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "et_second_half_added_time",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "cards",
                    models.ManyToManyField(
                        related_name="match_datas",
                        through="matches.MatchCards",
                        to="players.player",
                    ),
                ),
                (
                    "lineups",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_datas",
                        to="matches.lineup",
                    ),
                ),
                (
                    "match",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_datas",
                        to="matches.match",
                    ),
                ),
                (
                    "stadium",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_datas",
                        to="stadiums.stadium",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="matchcards",
            name="match_data",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="matches.matchdata"
            ),
        ),
        migrations.AddField(
            model_name="matchcards",
            name="player",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="players.player"
            ),
        ),
        migrations.AddField(
            model_name="lineup",
            name="reserved",
            field=models.ManyToManyField(
                related_name="match_reserved_lineups",
                through="matches.PlayerRole",
                to="players.player",
            ),
        ),
        migrations.CreateModel(
            name="Goals",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "half",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "First Half"),
                            (2, "Second Half"),
                            (3, "Extra Time First Half"),
                            (4, "Extra Time Second Half"),
                            (5, "Penalty Shoot-Out"),
                        ]
                    ),
                ),
                ("minute", models.PositiveIntegerField()),
                (
                    "goal_body_part",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Head"),
                            (2, "Left Foot"),
                            (3, "Right Foot"),
                            (9, "Other"),
                        ]
                    ),
                ),
                (
                    "assist_body_part",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (1, "Head"),
                            (2, "Left Foot"),
                            (3, "Right Foot"),
                            (9, "Other"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Progressive Pass"),
                            (2, "Basic Pass"),
                            (3, "Set Piece Pass"),
                            (4, "Set Piece Kick"),
                            (5, "Individual Play"),
                            (9, "Own Goal"),
                        ]
                    ),
                ),
                (
                    "area_of_shoot",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "6 Yard Box"),
                            (2, "Penalty Box"),
                            (3, "Outside Penalty Box"),
                        ]
                    ),
                ),
                (
                    "set_pieces_type",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (1, "Free Kick"),
                            (2, "Corner Kick"),
                            (3, "Penalty Kick"),
                            (4, "Throw In"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "attacking_flanks",
                    models.PositiveSmallIntegerField(
                        blank=True, choices=[(1, "Left"), (2, "Right")], null=True
                    ),
                ),
                ("is_deflected", models.BooleanField(default=False)),
                ("error_leading_to_goal", models.BooleanField(default=False)),
                (
                    "assist_pass_type",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (1, "Cross"),
                            (2, "Deep Completed Cross"),
                            (3, "Deflected Cross"),
                            (4, "Deep Completion"),
                            (5, "Head Pass"),
                            (6, "Progressive Pass"),
                            (90, "Rebound"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "assist",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goal_assists",
                        to="players.player",
                    ),
                ),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goals",
                        to="matches.match",
                    ),
                ),
                (
                    "scorer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goal_scorers",
                        to="players.player",
                    ),
                ),
                (
                    "second_assist",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goal_second_assists",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayerRoleProxy",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": [],},
            bases=("matches.playerrole",),
        ),
        migrations.AddField(
            model_name="lineup",
            name="starting",
            field=models.ManyToManyField(
                related_name="match_starting_lineups",
                through="matches.PlayerRoleProxy",
                to="players.player",
            ),
        ),
    ]
