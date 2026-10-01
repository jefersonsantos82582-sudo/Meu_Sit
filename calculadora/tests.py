from django.test import TestCase

from .models import Calculo
from .views import aplicar


class CalculadoraTests(TestCase):
    def test_operacoes(self):
        self.assertEqual(aplicar(2, 3, "+"), 5)
        self.assertEqual(aplicar(2, 3, "-"), -1)
        self.assertEqual(aplicar(2, 3, "*"), 6)
        self.assertEqual(aplicar(6, 3, "/"), 2)
        self.assertEqual(aplicar(2, 3, "**"), 8)

    def test_divisao_por_zero(self):
        self.assertEqual(aplicar(1, 0, "/"), "Erro")

    def test_api_calcular(self):
        resposta = self.client.post(
            "/api/calcular/",
            data='{"x": 2, "y": 8, "op": "*"}',
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["resultado"], "16")
        self.assertEqual(Calculo.objects.count(), 1)

    def test_api_operacao_invalida(self):
        resposta = self.client.post(
            "/api/calcular/",
            data='{"x": 2, "y": 8, "op": "?"}',
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 400)


from django.test import TestCase


class HomeTests(TestCase):
    def test_pagina_inicial(self):
        resposta = self.client.get("/")
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Calculadora")

    def test_post_sem_javascript(self):
        resposta = self.client.post("/", {"x": "2", "y": "3", "op": "+"})
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "5")
