# Generated by Django 3.2.2 on 2021-05-07 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeFiction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='content',
            field=models.TextField(max_length=9999, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.URLField(default='https://i.ibb.co/d400nvn/pp.png'),
        ),
        migrations.AlterField(
            model_name='story',
            name='description',
            field=models.TextField(default=None, max_length=250, unique=True),
        ),
    ]
