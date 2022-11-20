from django import forms
from ..models import Diarista
from ..services import cep_service
import json
import os

class DiaristaForm(forms.ModelForm):

    SEXO_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")
    )
   
    cpf = forms.CharField(widget=forms.TextInput(attrs={'data-mask': "000.000.000-00"}))
    cep = forms.CharField(widget=forms.TextInput(attrs={'data-mask': "00000-000"}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'data-mask': "(00) 00000-0000"}))
    sexo = forms.CharField(max_length=3,
                           widget=forms.Select(choices=SEXO_CHOICES))
    foto_usuario = forms.ImageField()
    #codigo_ibge = forms.IntegerField(required=False)

    
    class Meta:
        model = Diarista
        exclude = ('codigo_ibge', )

    def valida_nome(self):
        sexo = self.cleaned_data['sexo']
        foto_usuario = self.cleaned_data['foto_usuario']
        n = str(foto_usuario['foto_usuario']).split()[0]
        print(n)
        if str.upper(sexo) != str.upper(n):
            raise forms.ValidationError("nome errado")
       
      
    
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return cpf.replace(".", "").replace("-", "")

    def clean_cep(self):
        cep = self.cleaned_data['cep']
        cep_formatado = cep.replace("-", "")
        response = cep_service.buscar_cidade_cep(cep_formatado)
        if response.status_code == 400:
            raise forms.ValidationError("O CEP informado está incorreto")
        cidade_api = json.loads(response.content)
        if 'erro' in cidade_api:
            raise forms.ValidationError("O CEP informado não foi encontrado")
        return cep.replace("-", "")

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        return telefone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

    def save(self, commit=True):
        instance = super(DiaristaForm, self).save(commit=False)
        response = cep_service.buscar_cidade_cep(self.cleaned_data.get('cep'))
        cidade_api = json.loads(response.content)
        
        instance.codigo_ibge = cidade_api['ibge']
        instance.tipo_logradouro = str(cidade_api['logradouro']).split()[0]
        instance.logradouro = str(cidade_api['logradouro']).replace(
            instance.tipo_logradouro, '')
        instance.save()
        return instance