from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from core.models import Cliente, Veiculo, Parametro, \
                        Movimento, Mensalista
from core.forms import FormCliente, FormVeiculo, \
    FormParametro, FormMovimento, FormMensalista
# Create your views here.


def home(request):
    return render(request, 'core/index.html', {'acao': 'G4car - Estacionamentos'})


class Registrar(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


@login_required
def cadastro_cliente(request):
    form = FormCliente(request.POST or None, request.FILES or None)
    contexto = {'form': form, 'acao': 'Cadastro do cliente', 'titulo': 'Cadastrar cliente'}
    if form.is_valid():
        form.save()
        messages.success(request, "Cliente cadastrado com sucesso!")
        return redirect('url_listagem_clientes')
    else:
        return render(request, 'core/cadastro_cliente.html', contexto)


@login_required
def listagem_clientes(request):
    if request.POST:
        if request.POST['nome']:
            clientes = Cliente.objects.filter(nome=request.POST['nome'])
        else:
            clientes = Cliente.objects.all()
    else:
        clientes = Cliente.objects.all()
    contexto = {'clientes': clientes, 'acao': 'Lista de clientes'}
    return render(request, 'core/listagem_clientes.html', contexto)


@login_required
def cadastro_veiculo(request):
    form = FormVeiculo(request.POST or None, request.FILES or None)
    contexto = {'form': form, 'acao': 'Cadastro de veiculo', 'titulo': 'Atualizar cadastro'}
    if form.is_valid():
        form.save()
        messages.success(request, "Veiculo cadastrado com sucesso!")
        return redirect('url_listagem_veiculos')
    else:
        return render(request, 'core/cadastro_veiculo.html', contexto)


@login_required
def listagem_veiculos(request):
    if request.POST:
        if request.POST['modelo']:
            veiculos = Veiculo.objects.filter(modelo=request.POST['modelo'])
        else:
            veiculos = Veiculo.objects.all()
    else:
        veiculos = Veiculo.objects.all()
    contexto = {'veiculos': veiculos, 'acao': 'Lista de veiculos'}
    return render(request, 'core/listagem_veiculos.html', contexto)


@login_required
def atualiza_cliente(request, id):
    cliente_selecionado = Cliente.objects.get(id=id)
    form = FormCliente(request.POST or None, request.FILES or None, instance=cliente_selecionado)
    contexto = {'form': form, 'acao': 'Atualizar o cadastro do cliente', 'titulo': 'Atualizar cadastro'}
    if form.is_valid():
        form.save()
        messages.success(request, "Cliente atualizado com sucesso!")
        return redirect('url_listagem_clientes')
    else:
        return render(request, 'core/cadastro_cliente.html', contexto)


@login_required
def atualiza_veiculo(request, id):
    veiculo_selecionado = Veiculo.objects.get(id=id)
    form = FormVeiculo(request.POST or None, request.FILES or None, instance=veiculo_selecionado)
    contexto = {'form': form, 'acao': 'Atualizar o cadastro de veiculo', 'titulo': 'Atualizar cadastro'}
    if form.is_valid():
        form.save()
        messages.success(request, "Veiculo atualizado com sucesso!")
        return redirect('url_listagem_veiculos')
    else:
        return render(request, 'core/cadastro_veiculo.html', contexto)


@login_required
def exclui_cliente(request, id):
    try:
        cliente_selecionado = Cliente.objects.get(id=id)
        contexto = {'acao': cliente_selecionado.nome, 'redirect': '/listagem_clientes/'}
        if request.POST:
            cliente_selecionado.delete()
            return redirect('url_listagem_clientes')
        else:
            return render(request, 'core/confirma_exclusao.html', contexto)
    except:
        redirect('url_listagem_clientes')


@login_required
def exclui_veiculo(request, id):
    try:
        veiculo_selecionado = Veiculo.objects.get(id=id)
        if request.POST:
            veiculo_selecionado.delete()
            return redirect('url_listagem_veiculos')
        else:
            return render(request, 'core/confirma_exclusao.html', {'acao': veiculo_selecionado.modelo, 'redirect': '/listagem_veiculos/'})
    except:
        return redirect('url_listagem_veiculos')


@login_required
def cadastro_parametro(request):
    form = FormParametro(request.POST or None)
    contexto = {'form': form, 'acao': 'Cadastro de Parametro', 'titulo': 'Cadastro de Parametro'}
    if form.is_valid():
        form.save()
        messages.success(request, "Parametro cadastrado com sucesso!")
        return redirect('url_listagem_parametros')
    else:
        return render(request, 'core/cadastro_parametro.html', contexto)


@login_required
def listagem_parametros(request):
    if request.POST:
        if request.POST['codigo']:
            parametros = Parametro.objects.filter(id=request.POST['codigo'])
        else:
            parametros = Parametro.objects.all()
    else:
        parametros = Parametro.objects.all()
    contexto = {'parametros': parametros, 'acao': 'Tabela de preços'}
    return render(request, 'core/listagem_parametros.html', contexto)


@login_required
def cadastro_mensalista(request):
    form = FormMensalista(request.POST or None)
    contexto = {'form': form, 'acao': 'Cadastro de mensalista', 'titulo': 'Cadastro de mensalista'}
    if form.is_valid():
        form.save()
        messages.success(request, "Mensalista cadastrado com sucesso!")
        return redirect('url_listagem_mensalistas')
    else:
        return render(request, 'core/cadastro_mensalista.html', contexto)


@login_required
def listagem_mensalistas(request):
    if request.POST:
        if request.POST['codigo']:
            mensalista = Mensalista.objects.filter(id=request.POST['codigo'])
        else:
            mensalista = Mensalista.objects.all()
    else:
        mensalista = Mensalista.objects.all()
    contexto = {'mensalistas': mensalista, 'acao': 'Lista de mensalistas'}
    return render(request, 'core/listagem_mensalistas.html', contexto)


@login_required
def atualiza_mensalista(request, id):
    if request.user.is_staff:
        try:
            obj = Mensalista.objects.get(id=id)
            form = FormMensalista(request.POST or None, instance=obj)
            contexto = {'form': form, 'acao': 'Atualização de Mensalistas',
                        'titulo': 'Atualiza Mensalista - G4car'}
            if form.is_valid():
                form.save()
                messages.success(request, "Mensalista atualizado com sucesso!")
                return redirect('url_listagem_mensalistas')
            else:
                return render(request, 'core/cadastro_mensalista.html', contexto)
        except:
            return redirect('url_listagem_mensalistas')
    else:
        contexto = {'erro': 'Você não tem permissão para executar este procedimento, '
                            'procure o seu gerente.'}
        return render(request, 'core/erro.html', contexto)


@login_required
def exclui_mensalista(request, id):
    obj = Mensalista.objects.get(id=id)
    contexto = {'acao': obj.id_veiculo, 'redirect': '/listagem_mensalistas/'}
    if request.method == 'POST':
        obj.delete()
        return redirect('url_listagem_mensalistas')
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


@login_required
def atualiza_parametro(request, id):
    try:
        obj = Parametro.objects.get(id=id)
        form = FormParametro(request.POST or None, instance=obj)
        contexto = {'form': form, 'acao': 'Atualização de parametro'}
        if form.is_valid():
            form.save()
            messages.success(request, "Parametro atualizado com sucesso!")
            return redirect('url_listagem_parametros')
        else:
            return render(request, 'core/cadastro_parametro.html', contexto)
    except:
        return redirect('url_listagem_parametros')


@login_required
def exclui_parametro(request, id):
    obj = Parametro.objects.get(id=id)
    contexto = {'acao': obj.descricao, 'redirect': '/listagem_parametros/'}
    if request.method == 'POST':
        obj.delete()
        return redirect('url_listagem_parametros')
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


@login_required
def cadastro_movimento(request):
    if request.user.is_staff:
        form = FormMovimento(request.POST or None)
        contexto = {'form': form, 'titulo': 'Cadastro de movimento', 'acao': 'Cadastro de Movimento'}
        if form.is_valid():
            form.save()
            messages.success(request, "Movimento cadastrado com sucesso!")
            return redirect('url_listagem_movimentos')
        return render(request, 'core/cadastro_movimento.html', contexto)
    else:
        contexto = {'erro': 'Você não tem permissão para executar este procedimento, '
                            'procure o seu gerente.'}
        return render(request, 'core/erro.html', contexto)


@login_required
def listagem_movimentos(request):
    if request.POST:
        if request.POST['placa']:
            movimento = Movimento.objects.filter(id_veiculo__placa=request.POST['placa'])
        else:
            movimento = Movimento.objects.all()
    else:
        movimento = Movimento.objects.all()
    contexto = {'movimentos': movimento, 'acao': 'Lista de movimentos'}
    return render(request, 'core/listagem_movimentos.html', contexto)


@login_required
def atualiza_movimento(request, id):
    if request.user.is_staff:
        try:
            obj = Movimento.objects.get(id=id)
            form = FormMovimento(request.POST or None, instance=obj)
            contexto = {'form': form, 'acao': 'Atualização de Movimento',
                        'titulo': 'Atualiza Movimento - G4car'}
            if form.is_valid():
                retorno = obj.calcula_total()
                if retorno == 'erro':
                    contexto = {'erro': 'Valor de data de saída menor que de entrada,'
                                        ' favor realizar novamente'}
                    return render(request, 'core/erro.html', contexto)
                form.save()
                messages.success(request, "Movimento atualizado com sucesso!")
                return redirect('url_listagem_movimentos')
            else:
                return render(request, 'core/cadastro_movimento.html', contexto)
        except:
            return redirect('url_listagem_movimentos')
    else:
        contexto = {'erro': 'Você não tem permissão para executar este procedimento, '
                            'procure o seu gerente.'}
        return render(request, 'core/erro.html', contexto)


@login_required
def exclui_movimento(request, id):
    obj = Movimento.objects.get(id=id)
    contexto = {'acao': obj.id_veiculo, 'redirect': '/listagem_movimentos/'}
    if request.method == 'POST':
        obj.delete()
        return redirect('url_listagem_movimentos')
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)