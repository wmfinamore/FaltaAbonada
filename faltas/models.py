from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError

User = get_user_model()


class FaltaAbonada(models.Model):
    funcionario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Funcionário',
                                    related_name='faltas_usuario')
    data_falta = models.DateField(verbose_name='Data da Falta')

    @property
    def quantidade_faltas(self):
        faltas = FaltaAbonada.objects.filter(funcionario=self.funcionario)
        qt = 0
        for falta in faltas:
            if falta.data_falta.strftime("%Y") == date.today().strftime("%Y"):
                qt += 1
        return qt

    @property
    def abonou_no_mes(self):
        faltas_mes = FaltaAbonada.objects.filter(funcionario=self.funcionario)
        qt = 0
        for falta in faltas_mes:
            if falta.data_falta.strftime('%Y') == self.data_falta.strftime("%Y") \
                    and falta.data_falta.strftime('%m') == self.data_falta.strftime("%m"):
                qt += 1
        if qt:
            return True
        else:
            return False

    def clean(self):
        if self.abonou_no_mes:
            raise ValidationError('Você já abonou faltas no mês indicado')
        if self.quantidade_faltas >= 6:
            raise ValidationError('Você já usou todas as suas abonadas do ano')
        if self.data_falta.strftime("%Y") != date.today().strftime("%Y"):
            raise ValidationError('Você só pode registrar abonadas no ano corrente')

    def __str__(self):
        return self.funcionario.get_full_name() + ' - ' + str(self.data_falta)

    class Meta:
        ordering = ['funcionario', '-data_falta']
        verbose_name_plural = 'Faltas Abonadas'
