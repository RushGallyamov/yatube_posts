# Generated by Django 2.2.6 on 2021-03-18 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20210312_1843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]
