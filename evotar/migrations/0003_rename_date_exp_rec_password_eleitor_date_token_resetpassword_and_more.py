# Generated by Django 4.2.7 on 2023-11-25 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evotar', '0002_eleitor_date_exp_rec_password_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eleitor',
            old_name='date_exp_rec_password',
            new_name='date_token_resetpassword',
        ),
        migrations.RenameField(
            model_name='eleitor',
            old_name='token_rec_password',
            new_name='token_resetpassword',
        ),
    ]
