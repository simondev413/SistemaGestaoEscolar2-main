# Generated by Django 5.0.6 on 2024-06-17 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('carga_horaria', models.IntegerField(default=60, verbose_name='Carga Horária')),
                ('semestre', models.CharField(choices=[('1', '1º Semestre'), ('2', '2º Semestre')], max_length=20)),
            ],
        ),
    ]
