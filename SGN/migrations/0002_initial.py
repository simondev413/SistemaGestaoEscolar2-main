# Generated by Django 5.0.6 on 2024-06-17 14:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SGN', '0001_initial'),
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Professor',
                'verbose_name_plural': 'Professores',
            },
            bases=('user_auth.user',),
        ),
        migrations.CreateModel(
            name='Vaga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField()),
                ('tipo', models.CharField(choices=[('Funcionarios', 'Funcionarios'), ('Professores', 'Professores'), ('Estudantes', 'Estudantes')], max_length=120)),
                ('ano_academico', models.CharField(max_length=100, verbose_name='Ano Letivo')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='disciplina',
            unique_together={('nome', 'semestre')},
        ),
        migrations.CreateModel(
            name='Estudante',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGN.curso')),
            ],
            options={
                'verbose_name': 'Estudante',
                'verbose_name_plural': 'Estudantes',
            },
            bases=('user_auth.user',),
        ),
        migrations.CreateModel(
            name='ProfessorDisciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGN.disciplina')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGN.professor')),
            ],
        ),
        migrations.AddField(
            model_name='professor',
            name='disciplinas',
            field=models.ManyToManyField(related_name='professores', through='SGN.ProfessorDisciplina', to='SGN.disciplina'),
        ),
        migrations.CreateModel(
            name='FichaNota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prova1', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Prova 1')),
                ('avaliacao1', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Avaliação 1')),
                ('prova2', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Prova 2')),
                ('avaliacao2', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Avaliação 2')),
                ('exame', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Exame')),
                ('recurso', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Recurso')),
                ('media', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Média')),
                ('status', models.CharField(choices=[('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado'), ('Recurso', 'Recurso'), ('Dispensa', 'Dispensa'), ('Exame', 'Exame')], default='NaN', max_length=20)),
                ('estudante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGN.estudante')),
                ('professor_disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGN.professordisciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=60, null=True)),
                ('descricao', models.TextField()),
                ('turno', models.CharField(choices=[('Manhã', 'Manhã'), ('Tarde', 'Tarde'), ('Noite', 'Noite')], max_length=20)),
                ('ano_academico', models.CharField(choices=[('1', '1º Ano'), ('2', '2º Ano'), ('3', '3º Ano'), ('4', '4º Ano'), (5, '5º Ano')], max_length=10, verbose_name='Ano Acadêmico')),
                ('sala', models.PositiveIntegerField(verbose_name='Sala')),
                ('total_estudantes', models.PositiveIntegerField(default=0, verbose_name='Total de Estudantes')),
                ('limite', models.PositiveIntegerField(default=50, verbose_name='Número de estudantes')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGN.curso')),
            ],
            options={
                'unique_together': {('turno', 'sala', 'curso', 'ano_academico')},
            },
        ),
        migrations.AddField(
            model_name='professordisciplina',
            name='turma',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='SGN.turma'),
        ),
        migrations.AddField(
            model_name='estudante',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGN.turma'),
        ),
    ]
