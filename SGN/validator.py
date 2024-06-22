from django.core.exceptions import ValidationError

def validar_nota(value):
      if value < 0 or value > 20 :
        raise ValidationError(f'A nota {value} não é válida. Deve estar entre 0 e 20.')