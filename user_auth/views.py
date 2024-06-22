from django.urls import reverse_lazy
from django.shortcuts import redirect,render,HttpResponse,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from SGN.models import Estudante,Turma,Curso,Disciplina,ProfessorDisciplina,Professor,Vaga,FichaNota
from django import forms
from . import forms
from logs import models as logs_models
from .models import User

User = get_user_model()

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                if user.type == 'admin':
                    admin = User.objects.filter(email=email).first()
                    
                    log = logs_models.UserLogs.objects.create(texto=f'{admin} iniciou sessão.')
                    log.save()
                    return redirect('SGN:admin_dashboard')
                elif user.type == 'estudante':
                    return redirect('SGN:ver_fichas')
                elif user.type == 'professor':
                    return redirect('SGN:professor_perfil')
                else:
                    messages.error(request, 'Tipo de usuário não reconhecido.')
                    return redirect('user_auth:login')            
        return render(request,'user_auth/registration/login.html',{'error':'Dados inválidos'})
    return render(request,'user_auth/registration/login.html') 
                
def user_logout(request):
    if request.user.type == 'admin':
        log = logs_models.UserLogs.objects.create(texto=f'{request.user} terminou sessão.')
        log.save()
    logout(request)
    return redirect('index')

def registar_estudante(request):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        form = forms.EstudanteRegistrationForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():                
                curso = Curso.objects.filter(nome=form.cleaned_data['curso']).first()
                turma = Turma.objects.filter(curso=curso, turno=form.cleaned_data['turno'], ano_academico=form.cleaned_data['ano_academico']).first() 
                vagas = Vaga.objects.filter(tipo='Estudantes').first()
                if vagas.total > 0:
                    if turma.limite > 0: 
                        form.save()                       
                        turma.limite -= 1 
                        turma.total_estudantes += 1                       
                        vagas.total -= 1
                        turma.save()
                        vagas.save()                        
                        disciplinas = ProfessorDisciplina.objects.filter(turma=turma)                                            
                        estudante = Estudante.objects.filter(email=form.cleaned_data['email']).first()                        
                        ficha = FichaNota.objects.filter(estudante=estudante).first()
                        if not ficha:                                                        
                            for disciplina in disciplinas:
                                ficha = FichaNota.objects.create(estudante=estudante,professor_disciplina=disciplina,semestre=disciplina.disciplina.semestre)
                                ficha.save()
                        log = logs_models.UserLogs.objects.create(texto=f'Criado estudante {form.cleaned_data['nome']} {form.cleaned_data['sobrenome']}.')
                        log.save()
                        return redirect('SGN:admin_estudantes_dashboard')  
                        
                    return forms.ValidationError(f'Antigiu Limite de estudantes para a turma {turma}')        
                else:
                    return  forms.ValidationError(f'Não há vagas disponível para estudantes.')
                
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))  # Mostrar erros no navegador
        return render(request, 'user_auth/registration/registar_estudante.html', {'form': form})

def editar_estudante(request,pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        estudante = Estudante.objects.get(pk=pk)
        form = forms.EstudanteRegistrationForm(request.POST or None, request.FILES or None,instance=estudante)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                log = logs_models.UserLogs.objects.create(texto=f'Editado os dados do estudante {form.cleaned_data['nome']} {form.cleaned_data['sobrenome']}.')
                log.save()
                return redirect('SGN:admin_estudantes_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors)) 
        return render(request,'user_auth/registration/editar_estudante.html',{'form':form})

def del_estudante(request,pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:    
        estudante = get_object_or_404(Estudante,pk=pk)
        log = logs_models.UserLogs.objects.create(texto=f'Eliminado estudante {estudante.nome} {estudante.sobrenome}.')
        estudante_turma = Turma.objects.get(pk=estudante.turma.id)
        estudante_turma.total_estudantes -= 1
        estudante_turma.save()
        estudante.delete()
        log.save()
        return redirect('SGN:admin_estudantes_dashboard')

def registar_professor(request):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        form = forms.ProfessorRegistrationForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():            
                form.save()
                log = logs_models.UserLogs.objects.create(texto=f'Criado professor {form.cleaned_data['nome']} {form.cleaned_data['sobrenome']}.')
                log.save()
                return redirect('SGN:admin_professores_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors))  # Mostrar erros no navegador
        return render(request, 'user_auth/registration/registar_professor.html', {'form': form})

def editar_professor(request,pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        professor = Professor.objects.get(pk=pk)
        form = forms.ProfessorRegistrationForm(request.POST or None, request.FILES or None,instance=professor)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                log = logs_models.UserLogs.objects.create(texto=f'Editado os dados do professor {form.cleaned_data['nome']} {form.cleaned_data['sobrenome']}.')
                log.save()
                return redirect('SGN:admin_professores_dashboard')
            else:
                print(form.errors)  # Para depuração
                return HttpResponse('<p> Dados não validados: {}</p>'.format(form.errors)) 
        return render(request,'user_auth/registration/editar_professor.html',{'form':form,'professor':professor})

def del_professor(request,pk):
    if request.user.type != 'admin':
        return HttpResponse('Não tem permissão para acessar esta página.')
    else:
        professor = Professor.objects.get(pk=pk)
        log = logs_models.UserLogs.objects.create(texto=f'Eliminado professor {professor.nome} {professor.sobrenome}.')
        professor.delete()
        log.save()
        return redirect('SGN:admin_professores_dashboard')