# Generated by Django 4.0.3 on 2022-04-09 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('temple_island_bot', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
        migrations.RenameModel(
            old_name='UserWallets',
            new_name='UserWallet',
        ),
    ]