# Generated by Django 2.2 on 2020-06-16 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoup_app', '0006_auto_20200615_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='items',
            field=models.ManyToManyField(null=True, to='zoup_app.Item'),
        ),
    ]