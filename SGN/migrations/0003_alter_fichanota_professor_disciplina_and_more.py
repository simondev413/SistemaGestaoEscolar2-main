# Generated by Django 5.0.6 on 2024-06-17 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGN', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichanota',
            name='professor_disciplina',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='SGN.professordisciplina'),
        ),
        migrations.AlterUniqueTogether(
            name='fichanota',
            unique_together={('estudante', 'professor_disciplina')},
        ),
    ]