# Generated by Django 2.2.7 on 2019-11-16 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_delete_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityanswer',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='activityanswer',
            name='student',
        ),
        migrations.RemoveField(
            model_name='content',
            name='course',
        ),
        migrations.RemoveField(
            model_name='content',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='ActivityAnswer',
        ),
        migrations.DeleteModel(
            name='Content',
        ),
    ]