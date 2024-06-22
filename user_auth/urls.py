from django.urls import path
from . import  views

app_name = 'user_auth'

urlpatterns = [
    path('auth/login/', views.user_login, name='login'),
    path('auth/logout/',views.user_logout,name='logout'),

    path('auth/admin/registar/estudante',views.registar_estudante,name='registar_estudante'),
    path('auth/admin/editar/estudante/<int:pk>',views.editar_estudante,name='editar_estudante'),
    path('auth/admin/del/estudante/<int:pk>',views.del_estudante,name='deletar_estudante'),
    
    path('auth/admin/registar/professor',views.registar_professor,name='registar_professor'),
    path('auth/admin/editar/professor/<int:pk>',views.editar_professor,name='editar_professor'),
    path('auth/admin/del/professor/<int:pk>',views.del_professor,name='deletar_professor'),
]
