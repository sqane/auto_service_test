# Generated by Django 2.2.7 on 2019-11-20 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercar',
            name='rent_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Арендующий', to='autoservice.AS_user'),
        ),
    ]
