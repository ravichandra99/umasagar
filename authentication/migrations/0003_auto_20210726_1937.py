# Generated by Django 3.2.5 on 2021-07-26 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210723_1359'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Divison',
            new_name='Division',
        ),
        migrations.RenameField(
            model_name='division',
            old_name='divison',
            new_name='division',
        ),
    ]