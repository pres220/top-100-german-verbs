# Generated by Django 3.0 on 2019-12-07 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conjugator', '0007_mood_tense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conjugation',
            name='mood',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conjugator.Mood'),
        ),
        migrations.AlterField(
            model_name='conjugation',
            name='tense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conjugator.Tense'),
        ),
    ]