# Generated by Django 5.0.4 on 2024-04-25 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_users_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('token', models.CharField(max_length=5000)),
            ],
        ),
    ]