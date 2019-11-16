# Generated by Django 2.2.7 on 2019-11-14 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_delete_location'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='teacher',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='accounts.Teacher'),
            preserve_default=False,
        ),
    ]