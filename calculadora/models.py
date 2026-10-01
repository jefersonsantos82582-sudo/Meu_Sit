from django.db import models


class Calculo(models.Model):
    """Historico das operacoes feitas na calculadora."""

    x = models.FloatField()
    y = models.FloatField()
    operacao = models.CharField(max_length=8)
    resultado = models.CharField(max_length=64)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "calculo"
        verbose_name_plural = "calculos"

    def __str__(self):
        return "%s %s %s = %s" % (self.x, self.operacao, self.y, self.resultado)
