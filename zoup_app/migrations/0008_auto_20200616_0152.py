# Generated by Django 2.2 on 2020-06-16 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zoup_app', '0007_auto_20200616_0139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='menu',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='zoup_app.Menu'),
        ),
    ]
