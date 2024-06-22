from django import forms
from .models import User
from SGN.models import Estudante, Professor, Curso, Turma, Vaga,ProfessorDisciplina,Disciplina,FichaNota


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'nome', 'sobrenome', 'email', 'telefone', 'telefone2', 'endereco',
            'sexo', 'img'
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class AdminRegistrationForm(UserRegistrationForm):

    class Meta(UserRegistrationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = User.Type.ADMIN
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

class EstudanteRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class':'forms-field','placeholder':'Password'}))
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class':'forms-field','placeholder':'Confirme a Password'}))

    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), required=True, widget=forms.Select(attrs={'class':'forms-field'}))
    ano_academico = forms.ChoiceField(choices=[('1','1º Ano'), ('2','2º Ano'), ('3','3º Ano'), ('4','4º Ano'), ('5','5º Ano')], widget=forms.Select(attrs={'class':'forms-field'}))
    turno = forms.ChoiceField(choices=[('Manhã','Manhã'), ('Tarde','Tarde'), ('Noite','Noite')], widget=forms.Select(attrs={'class':'forms-field'}))
    sexo = forms.ChoiceField(choices=[('Masculino','Masculino'), ('Feminino','Feminino')], widget=forms.Select(attrs={'class':'forms-field'}))

    class Meta:
        model = Estudante
        fields = ['nome', 'sobrenome', 'email', 'telefone', 'telefone2', 'endereco', 'sexo', 'img', 'ano_academico', 'turno', 'curso']
        widgets = {
            'nome': forms.TextInput(attrs={'class':'forms-field','autofocus':'','placeholder':'Nome'}),
            'sobrenome': forms.TextInput(attrs={'class':'forms-field','placeholder':'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class':'forms-field','placeholder':'E-mail'}),
            'telefone': forms.TextInput(attrs={'class':'forms-field','placeholder':'Telefone'}),
            'telefone2': forms.TextInput(attrs={'class':'forms-field','placeholder':'Telefone 2 (Opcional)'}),
            'endereco': forms.TextInput(attrs={'class':'forms-field','placeholder':'Endereço'}),
            'img': forms.FileInput(attrs={'class':'forms-field'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return password2
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = User.Type.ESTUDANTE
        user.set_password(self.cleaned_data['password1'])
        curso = self.cleaned_data['curso']
        user.curso = curso
        ano_academico = self.cleaned_data['ano_academico']
        turno = self.cleaned_data['turno']
        turma = Turma.objects.filter(curso=curso, turno=turno, ano_academico=ano_academico).first()                
        user.turma = turma                        
        if commit:
            user.save()
            return user      

class ProfessorRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class':'forms-field','placeholder':'Password'}))
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class':'forms-field','placeholder':'Confirme a Password'}))

    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), required=True, widget=forms.Select(attrs={'class':'forms-field'}))
    ano_academico = forms.ChoiceField(choices=[('1','1º Ano'), ('2','2º Ano'), ('3','3º Ano'), ('4','4º Ano'), ('5','5º Ano')], widget=forms.Select(attrs={'class':'forms-field'}))
    turno = forms.ChoiceField(choices=[('Manhã','Manhã'), ('Tarde','Tarde'), ('Noite','Noite')], widget=forms.Select(attrs={'class':'forms-field'}))
    sexo = forms.ChoiceField(choices=[('Masculino','Masculino'), ('Feminino','Feminino')], widget=forms.Select(attrs={'class':'forms-field'}))
    semestre = forms.ChoiceField(choices=[('1º','1º Semestre'),('2º','2º Semestre')],widget=forms.Select(attrs={'class':'forms-field'}))
    disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.all(),widget=forms.Select(attrs={'class':'forms-field','placeholder':'Disciplina'}))
    class Meta(UserRegistrationForm.Meta):
        model = Professor
        fields = ['nome', 'sobrenome', 'email', 'telefone', 'telefone2', 'endereco', 'sexo', 'img', 'ano_academico','semestre','disciplina', 'turno', 'curso']
        widgets = {
            'nome': forms.TextInput(attrs={'class':'forms-field','autofocus':'','placeholder':'Nome'}),
            'sobrenome': forms.TextInput(attrs={'class':'forms-field','placeholder':'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class':'forms-field','placeholder':'E-mail'}),
            'telefone': forms.TextInput(attrs={'class':'forms-field','placeholder':'Telefone'}),
            'telefone2': forms.TextInput(attrs={'class':'forms-field','placeholder':'Telefone 2 (Opcional)'}),
            'endereco': forms.TextInput(attrs={'class':'forms-field','placeholder':'Endereço'}),
            'img': forms.FileInput(attrs={'class':'forms-field'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = User.Type.PROFESSOR
        user.set_password(self.cleaned_data['password1'])
        curso = self.cleaned_data['curso']
        user.curso = curso
        ano_academico = self.cleaned_data['ano_academico']
        turno = self.cleaned_data['turno']
        turma = Turma.objects.filter(curso=curso, turno=turno, ano_academico=ano_academico).first()          
        disciplina = Disciplina.objects.filter(nome=self.cleaned_data['disciplina']).first()   
        vagas = Vaga.objects.filter(tipo='Professores').first()  

        user.turma = turma
        if commit:        
            if vagas.total > 0:                                          
                user.save()
                vagas.total -= 1                     
                vagas.save()
                prof =Professor.objects.get(email=self.cleaned_data['email'])
                prof_disc = ProfessorDisciplina.objects.filter(professor=prof).first()
                if not prof_disc:
                    prof_disc = ProfessorDisciplina.objects.create(professor=user,disciplina=disciplina,turma=turma)
                    prof_disc.save()                    
                return user    
            return forms.ValidationError('Não há vagas para professores')

        