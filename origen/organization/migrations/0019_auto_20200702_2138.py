# Generated by Django 3.0.7 on 2020-07-03 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0018_merge_20200702_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='picture',
            new_name='org_avatar',
        ),
    ]
