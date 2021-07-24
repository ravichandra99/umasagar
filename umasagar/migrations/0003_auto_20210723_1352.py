# Generated by Django 3.2.5 on 2021-07-23 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import umasagar.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('umasagar', '0002_alter_salebilldetails_tcs'),
    ]

    operations = [
        migrations.AddField(
            model_name='salebill',
            name='user',
            field=models.ForeignKey(default='root', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='salebill',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salebilldetails',
            name='destination',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='varietycode',
            name='variety_code',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True, validators=[umasagar.validators.validate_pk]),
        ),
    ]
