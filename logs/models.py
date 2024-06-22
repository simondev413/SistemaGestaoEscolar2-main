from django.db import models
from django.utils import timezone
# Create your models here.
class UserLogs(models.Model):
    texto = models.TextField(max_length=500)
    data =  models.DateTimeField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.texto} - {self.data}'
    
    class Meta:
        ordering = ['-data']