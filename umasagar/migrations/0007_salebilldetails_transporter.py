# Generated by Django 3.2.5 on 2021-07-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umasagar', '0006_alter_salebilldetails_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='salebilldetails',
            name='transporter',
            field=models.CharField(default='First Last', max_length=50),
        ),
    ]