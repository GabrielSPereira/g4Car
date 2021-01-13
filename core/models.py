from math import ceil, floor, trunc
from django.db import models

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=100)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_clientes', blank=True, null=True)

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        verbose_name_plural = 'Clientes'


class Veiculo(models.Model):
    fabricante = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.CharField(max_length=4, blank=True, null=True)
    cor = models.CharField(max_length=20, blank=True, null=True)
    placa = models.CharField(max_length=10)
    id_cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_veiculos', blank=True, null=True)

    def __str__(self):
        return self.placa

    class Meta:
        verbose_name_plural = 'Veiculos'



class Parametro(models.Model):
    descricao = models.CharField(max_length=20)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.descricao}\n'

    class Meta:
        verbose_name_plural = 'Parâmetros'



class Movimento(models.Model):
    data_entrada = models.DateTimeField(auto_now_add=None)
    data_saida = models.DateTimeField(auto_now_add=None, blank=True, null=True)
    id_veiculo = models.ForeignKey("Veiculo", on_delete=models.CASCADE)
    valor_hora = models.ForeignKey("Parametro", on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'({self.id}) - {self.data_entrada} - {self.id_veiculo.placa}' \
               f' - - {self.id_veiculo.modelo} de cor {self.id_veiculo.cor}'

    class Meta:
        verbose_name_plural = 'Movimentos'

    def calcula_total(self):
        if self.data_saida:
            if self.data_saida < self.data_entrada:
                return 'erro'
            horas = (self.data_saida - self.data_entrada).total_seconds() / 3600
            minutos = (horas * 60) - (trunc(horas) * 60)
            if minutos > 15:
                horas = ceil(horas)
            else:
                horas = floor(horas)
            # obj = Parametro.objects.get(id=self.valor_hora) // caso for um parametro opcional
            self.total = horas * self.valor_hora.valor  # ai substitui por obj.valor
            return self.total
        return 0.0



class Mensalista(models.Model):
    mensalidade = models.ForeignKey("Parametro", on_delete=models.CASCADE)
    id_veiculo = models.ForeignKey("Veiculo", on_delete=models.CASCADE)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id_veiculo.placa} - ' \
               f'{self.id_veiculo.modelo} - - ' \
               f'Mensalidade - R${self.mensalidade.valor}'

    class Meta:
        verbose_name_plural = 'Mensalistas'