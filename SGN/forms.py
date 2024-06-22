from django import forms
from .models import Curso,Turma, Disciplina,Vaga,ProfessorDisciplina,FichaNota


class CursoRegistrationForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets={
            'nome':forms.TextInput(attrs={'placeholder':'Curso','autofocus':'','class':'forms-field'}),
            'descricao':forms.Textarea(attrs={'placeholder':'Descrição','class':'forms-field'}),
        }

class TurmaRegistraionForm(forms.ModelForm):
    class Meta :
        model = Turma
        fields = ['descricao','turno','curso','ano_academico','sala','limite']
        widgets ={
            # 'nome':forms.TextInput(attrs={'class':'forms-field','autofcocus':'','placeholder':'Nome'}),
            'descricao':forms.Textarea(attrs={'class':'forms-field','placeholder':'Descrição'}),
            'turno':forms.Select(attrs={'class':'forms-field','placeholder':'Descrição'}),
            'curso':forms.Select(attrs={'class':'forms-field','placeholder':'Curso'}),
            'ano_academico':forms.Select(attrs={'class':'forms-field','placeholder':'Ano acadêmico'}),
            'sala':forms.TextInput(attrs={'class':'forms-field','placeholder':'Sala'}),
            'limite':forms.TextInput(attrs={'class':'forms-field','placeholder':'Limite de alunos'}),
            

        }
    def save(self,commit=True):
        turma = super().save(commit=False)
        turma.total_estudantes = 0
        if commit:
            turma.save()
            return turma

class DisciplinaRegistrationForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'
        widgets = {
            'nome':forms.TextInput(attrs={'class':'forms-field','autofocus':'','placeholder':'Nome'}),
            'descricao':forms.Textarea(attrs={'class':'forms-field','placeholder':'Descrição'}),
            'carga_horaria':forms.TextInput(attrs={'class':'forms-field','placeholder':'Carga Horária'}),
            'semestre':forms.Select(attrs={'class':'forms-field','placeholder':'Semestre'}),
        }

class VagasForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = '__all__'
        widgets = {
            'total':forms.TextInput(attrs={'class':'forms-field','placeholder':'Número de vaga'}),
            'tipo':forms.Select(attrs={'class':'forms-field','placeholder':'Tipo'}),
            'ano_academico':forms.TextInput(attrs={'class':'forms-field','placeholder':'Ano Letivo'})
        }

class ProfessorDisciplinaForm(forms.Form):
    disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.all(),widget=forms.Select(attrs={'class':'forms-field','placeholder':'Disciplina'}))
    turma = forms.ModelChoiceField(queryset=Turma.objects.all(),widget=forms.Select(attrs={'class':'forms-field','placeholder':'Turma'}))

class FichaNotaForm(forms.ModelForm):
    class Meta:
        model = FichaNota
        fields = ['prova1','avaliacao1','prova2','avaliacao2','exame','recurso']
        widgets = {
            'prova1':forms.TextInput(attrs={'class':'forms-field','placeholder':'','autofocus':''}),
            'avaliacao1':forms.TextInput(attrs={'class':'forms-field','placeholder':''}),
            'prova2':forms.TextInput(attrs={'class':'forms-field','placeholder':''}),
            'avaliacao2':forms.TextInput(attrs={'class':'forms-field','placeholder':''}),
            'exame':forms.TextInput(attrs={'class':'forms-field','placeholder':''}),
            'recurso':forms.TextInput(attrs={'class':'forms-field','placeholder':''}),            
        }