# Generated by Django 4.1.7 on 2023-03-10 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities_bot', '0005_alter_user_used_citi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='used_citi',
            field=models.TextField(default='', null=True),
        ),
    ]