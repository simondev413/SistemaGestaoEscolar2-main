from django.db import models
from user_auth import models as user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from user_auth.models import User
from .validator import validar_nota

# Create your models here

class Curso(models.Model):
  nome = models.CharField(max_length=255)
  descricao = models.TextField()

  def __str__(self):
    return self.nome

class Disciplina(models.Model):
  nome = models.CharField(max_length=255)
  descricao = models.TextField(null=True,blank=True)
  carga_horaria = models.IntegerField(verbose_name = 'Carga Horária',default=60)
  semestre = models.CharField(max_length = 20, choices = [('1º Semestre','1º Semestre'),('2º Semestre','2º Semestre')])
  class Meta:
    unique_together = ['nome','semestre']

  def __str__(self):
    return self.nome

class Professor(user_model.User):
  disciplinas = models.ManyToManyField(Disciplina, related_name = 'professores',through='ProfessorDisciplina')
  
  class Meta:
    verbose_name = 'Professor'
    verbose_name_plural = 'Professores'
  def __str__(self):
    return self.nome

  def save(self, *args, **kwargs):
    self.type = User.Type.PROFESSOR
    super().save(*args, **kwargs)

class ProfessorDisciplina(models.Model):
  professor = models.ForeignKey(Professor,on_delete=models.CASCADE)  
  disciplina = models.ForeignKey(Disciplina,on_delete=models.CASCADE)
  turma = models.ForeignKey('SGN.Turma',on_delete=models.CASCADE, default='')


  class Meta:
    unique_together = ['professor','disciplina','turma']
  def __str__(self):
    return self.professor.nome + '  ' + self.professor.sobrenome + '-' + self.disciplina.nome 

class Turma(models.Model):
  nome = models.CharField(max_length=60,null=True,blank=True)
  descricao = models.TextField()
  turno = models.CharField(max_length=20,choices = [('Manhã','Manhã'),('Tarde','Tarde'),('Noite','Noite')])
  curso = models.ForeignKey(Curso,on_delete=models.CASCADE)
  ano_academico = models.CharField(verbose_name = 'Ano Acadêmico',choices = [('1','1º Ano'),('2','2º Ano'),('3','3º Ano'),('4','4º Ano'),('5','5º Ano')],max_length=10)
  sala = models.PositiveIntegerField(verbose_name = 'Sala')
  total_estudantes = models.PositiveIntegerField(verbose_name='Total de Estudantes',default=0)
  limite = models.PositiveIntegerField(default=50,verbose_name='Número de estudantes')
  def __str__(self):
    return self.nome

  class Meta:
    unique_together= ['turno','sala','curso','ano_academico']
    ordering = ['curso','ano_academico','turno']
  
  def save(self,*args,**kwargs): 
    def set_abr(nome=self.curso.nome, ano=self.ano_academico, turno=self.turno):
        iniciais = ''.join([palavra[0]  for palavra  in nome.split()]).upper()
        abr = f'{iniciais}{turno[0]}{ano}'
        return abr
    self.nome = set_abr()
    super().save(*args,**kwargs)

class Estudante(user_model.User):
  turma = models.ForeignKey(Turma,on_delete=models.CASCADE)
  curso = models.ForeignKey(Curso,on_delete=models.CASCADE)
  

  class Meta:
    verbose_name = 'Estudante'
    verbose_name_plural = 'Estudantes'
      
class FichaNota(models.Model):
    estudante = models.ForeignKey(Estudante,on_delete=models.CASCADE)
    professor_disciplina = models.ForeignKey(ProfessorDisciplina,on_delete=models.CASCADE,null=True,blank=True)
    prova1 = models.DecimalField(validators=[validar_nota],max_digits=5,decimal_places=2,verbose_name='Prova 1',null=True,blank=True)
    avaliacao1 = models.DecimalField(validators=[validar_nota],max_digits=5,decimal_places=2, verbose_name= 'Avaliação 1',null=True,blank=True)
    prova2 = models.DecimalField(validators=[validar_nota],max_digits=5,decimal_places=2,verbose_name= 'Prova 2',null=True,blank=True)
    avaliacao2 = models.DecimalField(validators=[validar_nota],max_digits=5,decimal_places=2, verbose_name= 'Avaliação 2',null=True,blank=True)
    exame = models.DecimalField(validators=[validar_nota],max_digits=5,decimal_places=2,verbose_name='Exame',null=True,blank=True)
    recurso = models.DecimalField(validators=[validar_nota],max_digits=5,decimal_places=2,verbose_name='Recurso',null=True,blank=True)
    media = models.DecimalField(validators=[validar_nota],max_digits=5,decimal_places=2,verbose_name='Média',null=True,blank=True)
    status = models.CharField(max_length=20,choices = [('Aprovado','Aprovado'),('Reprovado','Reprovado'),('Recurso','Recurso'),('Dispensa','Dispensa'),('Exame', 'Exame')],default='Não avaliado')
    semestre = models.CharField(max_length=20,choices=[('1º Semestre','1º Semestre'),('2º Semestre','2º Semestre')],default='1º Semestre')
    def __str__(self):
      return self.estudante.nome + '  ' + self.estudante.sobrenome 
    class Meta:
      unique_together = ['estudante','professor_disciplina']  
 
    

class Vaga(models.Model):
  class Tipo(models.TextChoices):
    FUNC = 'Funcionarios','Funcionarios'
    PROF = 'Professores','Professores'
    ESTUDANTE = 'Estudantes','Estudantes'
  total = models.PositiveIntegerField()
  tipo = models.CharField(max_length=120,choices=Tipo.choices)
  ano_academico = models.CharField(max_length=100,verbose_name = 'Ano Letivo')

  def __str__(self):
    return f'{self.total}'