from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from . import forms
from logs import models as logs_models
from django.core.mail import send_mail
from django.conf import settings



@login_required(login_url='user_auth:login')
def dashboard(request):
    if request.user.type == 'admin':
        vagas = Vaga.objects.all()
        if not vagas:
            vagas_professor = Vaga.objects.create(total=500,tipo='Professores')    
            vagas_professor.save()
            vagas_estudantes = Vaga.objects.create(total=500,tipo='Estudantes')
            vagas_estudantes.save()
            vagas_funcionarios = Vaga.objects.create(total=500,tipo='Funcionarios')
            vagas_funcionarios.save()
        filtro_log =  request.GET.get('log_data')
        estudantes = Estudante.objects.all()
        professores = Professor.objects.all()
        turmas = Turma.objects.all()
        cursos = Curso.objects.all()
        discplinas = Disciplina.objects.all()
        fichas = FichaNota.objects.all()
        if filtro_log:
            logs = logs_models.UserLogs.objects.filter(data__icontains=filtro_log)
        else:
            logs = logs_models.UserLogs.objects.all()        
        context = {
            'estudantes':estudantes,
            'professores': professores,
            'turmas': turmas,
            'cursos':cursos,
            'disciplinas':discplinas,
            'fichas': fichas,
            'logs': logs,
        
        }
        return render(request,'SGN/index.html',context)
    return HttpResponse('Não tem permissão para acessar esta página.')

@login_required(login_url='user_auth:login')
def ver_fichas(request):
    if request.user.type == 'estudante':
        semestre_filtro = request.GET.get('semestre')
        estudante = Estudante.objects.get(pk=request.user.id)  
        if semestre_filtro:  
            fichas = FichaNota.objects.all().filter(estudante=estudante,semestre=semestre_filtro)       
        else:            
            fichas =  FichaNota.objects.all().filter(estudante=estudante)
        context = {'estudante':estudante,'fichas':fichas}
        template_name = 'SGN/estudantes/ver_fichas.html'
        return render(request,template_name,context)
    return HttpResponse('Não tem permissão para acessar esta página.')

@login_required(login_url='user_auth:login')
def  get_estudantes(request):
    if request.user.type == 'admin':
        vagas = Vaga.objects.filter(tipo='Estudantes').first()
        filtro = request.GET.get('nome_aluno')    
    
        if filtro:
            estudantes = Estudante.objects.filter(nome__icontains=filtro) or Estudante.objects.filter(sobrenome__icontains=filtro)
        else:
            estudantes = Estudante.objects.all()
        
        context = {'estudantes':estudantes,'vagas':vagas}
        template_name = 'SGN/admin_estudantes_dashboard.html'
        return render(request,template_name,context)
    return HttpResponse('Não tem permissão para acessar esta página.')

@login_required(login_url='user_auth:login')
def estudante_perfil(request,estudante_pk):
    if request.user.type == 'admin':
        semestre_filtro = request.GET.get('semestre')
        estudante = Estudante.objects.get(pk=estudante_pk)  
        if semestre_filtro:  
            fichas = FichaNota.objects.all().filter(estudante=estudante,semestre=semestre_filtro)       
        else:            
            fichas =  FichaNota.objects.all().filter(estudante=estudante)
        context = {'estudante':estudante,'fichas':fichas}
        template_name = 'SGN/estudantes/estudante_perfil.html'
        return render(request,template_name,context)
    return HttpResponse('Não tem permissão para acessar esta página.')

@login_required(login_url='user_auth:login')
def  get_professores(request):
    if request.user.type == 'admin':
        vagas = Vaga.objects.filter(tipo='Professores').first()
        filtro = request.GET.get('nome_professor')    
    
        if filtro:
            professores = Professor.objects.filter(nome__icontains=filtro,sobrenome__icontains=filtro) 
            
        else:
            professores = Professor.objects.all()
        prof_disciplina = ProfessorDisciplina.objects.all()

        context = {'professores':professores,'prof_disc':prof_disciplina,'vagas':vagas}
        template_name = 'SGN/admin_professores_dashboard.html'
        return render(request,template_name,context)
    return HttpResponse('Não tem permissão para acessar esta página.')

@login_required(login_url='user_auth:login')
def admin_professor_perfil(request,professor_pk):
    if request.user.type == 'admin':        
        professor =Professor.objects.get(pk=professor_pk)
        disciplinas = ProfessorDisciplina.objects.filter(professor=professor_pk)
        context = {'professor':professor,'disciplinas':disciplinas}
        template_name = 'SGN/professores/admin_professor_perfil.html'
        return render(request,template_name,context)
    return HttpResponse('Não tem permissão para acessar está página.')

@login_required(login_url='user_auth:login')
def atribuir_disciplina(request,professor_pk):
    if request.user.type == 'admin':     
        professor = Professor.objects.get(pk=professor_pk)  
        form = forms.ProfessorDisciplinaForm(request.POST or None)                  
        if request.method == 'POST':
            if form.is_valid(): 
                disciplina = Disciplina.objects.get(nome=form.cleaned_data['disciplina'])           
                turma = Turma.objects.get(nome=form.cleaned_data['turma'])   
                ProfessorDisciplina.objects.create(professor=professor,disciplina=disciplina,turma=turma).save()
                
                return redirect('SGN:admin_professor_perfil',professor_pk)
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        context = {'form':form,'professor':professor}          
        template_name = 'SGN/professores/professor_disciplina.html'
        return render(request,template_name,context)

@login_required(login_url='user_auth:login')
def editar_professor_disciplina(request,professor_disciplina_pk):
    if request.user.type == 'admin':  
        professor_disciplina = ProfessorDisciplina.objects.get(pk=professor_disciplina_pk)
        professor = professor_disciplina.professor
        form = forms.ProfessorDisciplinaForm(request.POST or None)                      
        if request.method == 'POST':
            if form.is_valid(): 
                disciplina = Disciplina.objects.get(nome=form.cleaned_data['disciplina'])           
                turma = Turma.objects.get(nome=form.cleaned_data['turma'])   
                professor_disciplina.disciplina=disciplina
                professor_disciplina.turma=turma               
                professor_disciplina.save()
                return redirect('SGN:admin_professor_perfil',professor.id)
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        context = {'form':form,'professor':professor}          
        template_name = 'SGN/professores/professor_disciplina.html'
        return render(request,template_name,context)

@login_required(login_url='user_auth:login')
def professor_perfil(request):
    if request.user.type =='professor':
        professor =Professor.objects.get(pk=request.user.id)
        disciplinas = ProfessorDisciplina.objects.filter(professor=professor.pk)
        context = {'professor':professor,'disciplinas':disciplinas}
        template_name = 'SGN/professores/professor_perfil.html'
        return render(request,template_name,context)
    return HttpResponse('Não tem permissão para acessar está página.')

@login_required(login_url='user_auth:login')
def lancar_notas(request,turma_pk,disciplina_pk):
    if request.user.type == 'professor':
        if request.method =='GET':   
            disciplina =Disciplina.objects.get(pk=disciplina_pk)  
            turma = Turma.objects.get(pk=turma_pk)
            professor_disciplina = ProfessorDisciplina.objects.filter(professor=request.user.id,disciplina=disciplina_pk,turma =turma_pk).first()                   
            fichas = FichaNota.objects.filter(professor_disciplina=professor_disciplina)
            alunos_avaliados =FichaNota.objects.filter(professor_disciplina=professor_disciplina).count() - FichaNota.objects.filter(professor_disciplina=professor_disciplina,status='Não avaliado').count()
            context = {'fichas':fichas,'disciplina':disciplina,'turma':turma,'alunos_avaliados':alunos_avaliados}   
            template_name ='SGN/professores/lancar_notas.html' 
            return render(request, template_name,context)                 
    return HttpResponse('Não tem permissão para acessar esta página.')

@login_required(login_url='user_auth:login')
def avaliar_aluno(request,estudante_pk,disciplina_pk):
    if request.user.type == 'professor':
        estudante = Estudante.objects.get(pk=estudante_pk)
        professor_disciplina = ProfessorDisciplina.objects.filter(professor=request.user.id,disciplina=disciplina_pk,turma=estudante.turma.id).first()                   
        ficha = FichaNota.objects.filter(estudante=estudante,professor_disciplina=professor_disciplina).first()
        form = forms.FichaNotaForm(request.POST or None,instance=ficha)       
        if request.method == 'POST':
            if form.is_valid():               
                form.save()
                prova1 = ficha.prova1 if ficha.prova1 is not None else 0
                prova2 = ficha.prova2 if ficha.prova2 is not None else 0
                if  ficha.prova1_ajustada:
                    ficha.avaliacao1 =0          
                    ficha.avaliacao2 = 0               
                    # Ajusta proif not ficha.prova1_ajustada and ficha.avaliacao1 is not None:
                if ficha.avaliacao1 > prova1:
                    prova1 = (prova1 + ficha.avaliacao1) / 2
                ficha.prova1_ajustada = True
        
                # Ajusta prova2 com avaliacao2 se aplicável e se ainda não foi ajustada
                if not ficha.prova2_ajustada and ficha.avaliacao2 is not None and prova2 > 0:
                    if ficha.avaliacao2 > prova2:
                        prova2 = (prova2 + ficha.avaliacao2) / 2
                    ficha.prova2_ajustada = True
                    
                # Calcula a média das provas
                media_provas = (prova1 + prova2) / 2 if prova2 > 0 else prova1/2
                
                # Determina o status baseado na média das provas, se o status não estiver finalizado
                if not ficha.status_finalizado:
                    if media_provas >= 13.5:
                        if media_provas < 13.9:
                            media_provas = 14.0  # Arredonda para 14
                        ficha.status = 'Dispensa'
                        ficha.exame = None
                        ficha.recurso = None
                        ficha.status_finalizado = True  # Finaliza o status
                    elif 7 <= media_provas < 13.5:
                        ficha.status = 'Exame'
                    else:
                        ficha.status = 'Recurso'

                # Verifica se o exame foi realizado e o status não estiver finalizado
                if ficha.exame is not None and not ficha.status_finalizado:
                    media_final = (float(media_provas) * 0.4) + (float(ficha.exame) * 0.6)
                    ficha.status = 'Aprovado' if media_final >= 10 else 'Recurso'
                    ficha.media = media_final
                    ficha.status_finalizado = ficha.status == 'Aprovado'  # Finaliza o status se aprovado
                else:
                    ficha.media = media_provas

                # Verifica se o recurso foi realizado e o status não estiver finalizado
                if ficha.recurso is not None and not ficha.status_finalizado:
                    ficha.media = ficha.recurso
                    ficha.status = 'Aprovado' if ficha.recurso >= 10 else 'Reprovado'
                    ficha.status_finalizado = ficha.status == 'Aprovado'  # Finaliza o status se aprovado

                # Salva o status e a média atualizada no banco de dados
                if ficha.exame is not None:
                    if ficha.media > 10:
                        ficha.recurso = None 
                ficha.save()


                
                return redirect('SGN:lancar_notas',estudante.turma.id,professor_disciplina.disciplina.id)
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        context = {'form':form,'estudante':estudante,'disciplina':professor_disciplina.disciplina}  
        template_name = 'SGN/professores/estudantes_notas.html'
        return render(request,template_name,context)
    
# CURSOS
@login_required(login_url='user_auth:login')
def get_cursos(request):
    if request.user.type == 'admin':
        filtro_curso = request.GET.get('nome_curso')
        if  filtro_curso:
            cursos = Curso.objects.filter(nome__icontains=filtro_curso)
        else:
            cursos = Curso.objects.all()
        context ={'cursos':cursos}
        template_name = 'SGN/admin_cursos_dashboard.html'
        return render(request,template_name,context)
    return HttpResponse('Não tem permissão para acessar esta página.')

@login_required(login_url='user_auth:login')
def registrar_curso(request):
    if request.user.type == 'admin':
        form = forms.CursoRegistrationForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                log = logs_models.UserLogs.objects.create(texto=f'Criado o curso {form.cleaned_data['nome']}.')            
                form.save()
                log.save()
                return redirect('SGN:admin_cursos_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        context ={'form':form}
        template_name = 'SGN/cursos/registrar_curso.html'
        return render(request,template_name,context)
    return HttpResponse('Não tem permissão para acessar esta página.')

@login_required(login_url='user_auth:login')
def editar_curso(request,curso_pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        curso = Curso.objects.get(pk=curso_pk)
        form = forms.CursoRegistrationForm(request.POST or None,instance=curso)
        if request.method == 'POST':
            if form.is_valid():
                log = logs_models.UserLogs.objects.create(texto=f'Editado o curso {curso.nome}.')
                form.save()
                log.save()
                return redirect('SGN:admin_cursos_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        context ={'form':form}
        template_name = 'SGN/cursos/editar_curso.html'
        return render(request,template_name,context)

@login_required(login_url='user_auth_login')
def del_curso(request,curso_pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        curso = Curso.objects.get(pk=curso_pk)
        log = logs_models.UserLogs.objects.create(texto=f'Eliminado o curso {curso.nome}.')
        curso.delete()
        log.save()
        return redirect('SGN:admin_cursos_dashboard')


# TURMAS
@login_required(login_url='user_auth:login')
def get_turmas(request):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        filtro_turma = request.GET.get('filtro_turma')
        if  filtro_turma:
            curso = Curso.objects.filter(nome__icontains=filtro_turma).first()
            if curso:
                turmas =Turma.objects.filter(curso=curso.id)
            else:
                turmas =  Turma.objects.filter(nome__icontains=filtro_turma)
        else:
            turmas = Turma.objects.all()
        context ={'turmas':turmas}
        template_name = 'SGN/admin_turmas_dashboard.html'

        return render(request,template_name,context)

@login_required(login_url='user_auth:login')
def registrar_turma(request):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        form = forms.TurmaRegistraionForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                turma = form.Meta.model.objects.filter(curso=form.cleaned_data['curso'],turno=form.cleaned_data['turno'],ano_academico=form.cleaned_data['ano_academico']).first()
                log = logs_models.UserLogs.objects.create(texto=f'Criada a turma {turma.nome}.')
                log.save()
                return redirect('SGN:admin_turmas_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        context ={'form':form}
        template_name = 'SGN/turmas/registrar_turma.html'
        return render(request,template_name,context)

@login_required(login_url='user_auth:login')
def editar_turma(request,turma_pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        turma = Turma.objects.get(pk=turma_pk)
        form = forms.TurmaRegistraionForm(request.POST or None,instance=turma)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                log = logs_models.UserLogs.objects.create(texto=f'Editado a turma {turma.nome}.')
                log.save()
                return redirect('SGN:admin_turmas_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        context ={'form':form}
        template_name = 'SGN/turmas/editar_turma.html'
        return render(request,template_name,context)

@login_required(login_url='user_auth_login')
def del_turma(request,turma_pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        turma = Turma.objects.get(pk=turma_pk)
        log = logs_models.UserLogs.objects.create(texto=f'Eliminada a turma {turma.nome}.')
        turma.delete()
        log.save()
        return redirect('SGN:admin_turmas_dashboard')


# DISCICIPLINAS
@login_required(login_url='user_auth_login')
def get_disciplinas(request):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:    
        filtro_disciplina = request.GET.get('nome_disciplina')

        if filtro_disciplina:
            disciplinas = Disciplina.objects.filter(nome__icontains=filtro_disciplina)
        else:
            disciplinas = Disciplina.objects.all()
        template_name = 'SGN/admin_disciplinas_dashboard.html'
        context = {'disciplinas':disciplinas}
        return render(request,template_name,context)

@login_required(login_url='user_auth_login')
def registrar_disciplina(request):

    if request.user.type !='admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        form = forms.DisciplinaRegistrationForm(request.POST or None)
        template_name = 'SGN/disciplinas/registrar_disciplina.html'
        context = {'form':form}
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                log = logs_models.UserLogs.objects.create(texto=f'Criada a disciplina {form.cleaned_data['nome']}.')
                log.save()
                return redirect('SGN:admin_disciplinas_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        return render(request,template_name,context)
        
@login_required(login_url='user_auth_login')
def editar_disciplina(request,disciplina_pk):

    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        disciplina = Disciplina.objects.get(pk=disciplina_pk)
        form = forms.DisciplinaRegistrationForm(request.POST or None,instance=disciplina)
        template_name = 'SGN/disciplinas/editar_disciplina.html'
        context = {'form':form}
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                log = logs_models.UserLogs.objects.create(texto=f'Editada a disciplina {disciplina.nome}.')
                log.save()
                return redirect('SGN:admin_disciplinas_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        return render(request,template_name,context)

@login_required(login_url='user_auth:login')
def del_disciplina(request,disciplina_pk):
    
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        disciplina =Disciplina.objects.get(pk=disciplina_pk)
        log = logs_models.UserLogs.objects.create(texto=f'Eliminada a disciplina {disciplina.nome}.')
        disciplina.delete()
        log.save()
        return redirect('SGN:admin_disciplinas_dashboard')
        
@login_required(login_url='user_auth:login')
def vagas(request):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        vagas = Vaga.objects.all()
        context={'vagas':vagas}
        template_name = 'SGN/vagas/vagas.html'
        return render(request,template_name,context)

@login_required(login_url='user_auth:login')
def set_vagas(request,vaga_pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        vaga = Vaga.objects.get(pk=vaga_pk)
        form = forms.VagasForm(request.POST or None,instance=vaga)
        context = {'form':form}
        template_name ='SGN/vagas/set_vagas.html'
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                log = logs_models.UserLogs.objects.create(texto=f'Criada uma nova vaga para {form.cleaned_data['total']} {form.cleaned_data['tipo']}.')
                log.save()
                return redirect('SGN:vagas')
            else:    
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))
        return render(request,template_name,context)
