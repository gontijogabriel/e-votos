# Generated by Django 4.2.7 on 2023-11-25 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evotar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eleitor',
            name='date_exp_rec_password',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eleitor',
            name='date_exp_valid_vote',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eleitor',
            name='token_rec_password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='eleitor',
            name='token_valid_vote',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]