# Generated by Django 5.0.4 on 2024-06-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_users_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='number',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
