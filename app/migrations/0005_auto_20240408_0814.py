# Generated by Django 3.2.4 on 2024-04-08 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20240309_0544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locationdata',
            old_name='is_sent',
            new_name='is_aggr',
        ),
        migrations.AddField(
            model_name='locationdata',
            name='obj',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locationdata',
            name='rsrq',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locationdata',
            name='rssnr',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='locationdata',
            name='Operator',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='locationdata',
            name='Users',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
