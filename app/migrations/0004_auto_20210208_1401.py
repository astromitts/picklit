# Generated by Django 3.1.6 on 2021-02-08 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210208_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='datatabledefinition',
            name='rows',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='step',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.datatabledefinition'),
        ),
        migrations.DeleteModel(
            name='DataTable',
        ),
    ]