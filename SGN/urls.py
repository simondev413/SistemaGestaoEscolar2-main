from django.urls import path 
from . import views

app_name = 'SGN'
 

urlpatterns = [
    path('sgn/admin/dashboard/', views.dashboard, name='admin_dashboard'),

    path('sgn/admin/dashboard/estudantes',views.get_estudantes,name='admin_estudantes_dashboard'),
    path('sgn/admin/dashboard/estudante/<int:estudante_pk>/perfil',views.estudante_perfil,name='estudante_perfil'),

    path('sgn/admin/dashboard/professores',views.get_professores,name='admin_professores_dashboard'),
    path('sgn/admin/dashboard/professor/<int:professor_pk>/perfil',views.admin_professor_perfil,name='admin_professor_perfil'),
    path('sgn/admin/dashboard/professor/<int:professor_pk>/disciplina',views.atribuir_disciplina,name='atribuir_disciplina'),
    path('sgn/admin/dashboard/professor/disciplina/editar/<int:professor_disciplina_pk>',views.editar_professor_disciplina,name='editar_professor_disciplina'),
    
    path('sgn/admin/dashboard/cursos',views.get_cursos,name='admin_cursos_dashboard'),
    path('sgn/admin/dashboard/cursos/registrar',views.registrar_curso,name='registrar_curso'),
    path('sgn/admin/dashboard/cursos/editar/<int:curso_pk>',views.editar_curso,name='editar_curso'),
    path('sgn/admin/dashboard/cursos/deletar/<int:curso_pk>',views.del_curso,name='deletar_curso'),
    
    path('sgn/admin/dashboard/turmas',views.get_turmas,name='admin_turmas_dashboard'),
    path('sgn/admin/dashboard/turma/registrar',views.registrar_turma,name='registrar_turma'),
    path('sgn/admin/dashboard/turma/editar/<int:turma_pk>',views.editar_turma,name='editar_turma'),
    path('sgn/admin/dashboard/turma/deletar/<int:turma_pk>',views.del_turma,name='deletar_turma'),
    
    path('sgn/admin/dashboard/disciplinas',views.get_disciplinas,name='admin_disciplinas_dashboard'),
    path('sgn/admin/dashboard/disciplina/registrar',views.registrar_disciplina,name='registrar_disciplina'),
    path('sgn/admin/dashboard/disciplina/editar/<int:disciplina_pk>',views.editar_disciplina,name='editar_disciplina'),
    path('sgn/admin/dashboard/disciplina/deletar/<int:disciplina_pk>',views.del_disciplina,name='deletar_disciplina'),
    
    path('sgn/admin/dashboard/vagas',views.vagas,name='vagas'),
    path('sgn/admin/dashboard/vaga/<int:vaga_pk>',views.set_vagas,name='set_vagas'),
    
    
    path('sgn/professor/lancar_notas/turma/<int:turma_pk>/disciplina/<int:disciplina_pk>', views.lancar_notas, name='lancar_notas'),
    path('sgn/professor/lancar_notas/estudante/<int:estudante_pk>/disciplina/<int:disciplina_pk>', views.avaliar_aluno, name='avaliar_aluno'),
    path('sgn/professor/perfil', views.professor_perfil, name='professor_perfil'),
   
    path('sgn/estudante/perfil', views.ver_fichas, name='ver_fichas'),
]
