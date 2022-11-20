from django.db import models

# Create your models here.

class Diarista(models.Model):
    SEXO_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")
    )


    nome_completo = models.CharField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    telefone = models.CharField(max_length=11, null=False, blank=False)
    tipo_logradouro = models.CharField(max_length=11, null=False, blank=False)
    logradouro = models.CharField(max_length=60, null=False, blank=False)
    numero = models.IntegerField(null=False, blank=False)
    complemento = models.CharField(max_length=100, null=False, blank=True)
    bairro = models.CharField(max_length=30, null=False, blank=False)
    cep = models.CharField(max_length=8, null=False, blank=False)
    cidade = models.CharField(max_length=30, null=False, blank=True)
    estado = models.CharField(max_length=2, null=False, blank=False)
    codigo_ibge = models.IntegerField(null=False, blank=False)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False, null=False)
    foto_usuario = models.ImageField(null=False)
