# Generated by Django 4.2.7 on 2023-11-27 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evotar', '0007_alter_eleicao_data_fim_alter_eleicao_data_inicio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eleitor',
            old_name='token_resetpassword',
            new_name='date_token',
        ),
        migrations.RenameField(
            model_name='eleitor',
            old_name='token_valid_vote',
            new_name='token_valid',
        ),
        migrations.RemoveField(
            model_name='eleitor',
            name='date_exp_valid_vote',
        ),
        migrations.RemoveField(
            model_name='eleitor',
            name='date_token_resetpassword',
        ),
    ]
