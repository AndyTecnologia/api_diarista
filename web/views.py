from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import diarista_form
from .models import Diarista
import os

# Create your views here.

def cadastrar_diarista(request):
    if request.method == "POST":
        form_diarista = diarista_form.DiaristaForm(request.POST, request.FILES)
        if form_diarista.is_valid():
            sexo = form_diarista['sexo'].value()
            nome = form_diarista.cleaned_data['foto_usuario'].name
            n = os.path.splitext(nome)[0]
            if str.upper(sexo) != str.upper(n):
                messages.error(request, 'Erro')
                return redirect('listar_diaristas')
            else:
                form_diarista.save()
                messages.success(request, 'cadastro Realizado')
                return redirect('listar_diaristas')
    else:
        form_diarista = diarista_form.DiaristaForm()
    return render(request, 'form_diarista.html', {'form_diarista': form_diarista})


def listar_diaristas(request):
    diaristas = Diarista.objects.all()
    return render(request, 'lista_diaristas.html', {'diaristas': diaristas})


def editar_diarista(request, diarista_id):
    diarista = Diarista.objects.get(id=diarista_id)
    if request.method == "POST":
        form_diarista = diarista_form.DiaristaForm(request.POST or None, request.FILES, instance=diarista)
        if form_diarista.is_valid():
            form_diarista.save()
            return redirect('listar_diaristas')
    else:
        form_diarista = diarista_form.DiaristaForm(instance=diarista)
    return render(request, 'form_diarista.html', {'form_diarista': form_diarista})


def remover_diarista(request, diarista_id):
    diarista = Diarista.objects.get(id=diarista_id)
    diarista.delete()
    return redirect('listar_diaristas')