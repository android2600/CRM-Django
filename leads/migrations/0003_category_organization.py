# Generated by Django 3.1.4 on 2023-02-14 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_auto_20230214_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]
