# Generated by Django 5.0.4 on 2024-05-04 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_address_alter_user_college_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='email',
        ),
    ]
