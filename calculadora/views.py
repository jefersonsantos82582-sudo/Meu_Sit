from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Calculo

OPERACOES = ("+", "-", "*", "/", "**")


def aplicar(x, y, op):
    """Mesma matematica da versao original (Django + template)."""
    if op == "+":
        return x + y
    if op == "-":
        return x - y
    if op == "*":
        return x * y
    if op == "/":
        return x / y if y != 0 else "Erro"
    if op == "**":
        return x ** y
    raise ValueError("Operacao invalida: %s" % op)


def formatar(valor):
    if isinstance(valor, str):
        return valor
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def _converter(valor):
    try:
        return float(Decimal(str(valor)))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Numero invalido")


def registrar(x, y, op, resultado):
    try:
        Calculo.objects.create(
            x=x, y=y, operacao=op, resultado=formatar(resultado)
        )
    except Exception:  # o calculo nao pode falhar porque o log falhou
        pass


def home(request):
    """Renderiza a pagina. Segue aceitando POST como fallback sem JavaScript."""
    resultado = None

    if request.method == "POST":
        try:
            x = float(request.POST["x"])
            y = float(request.POST["y"])
            op = request.POST["op"]
            resultado = aplicar(x, y, op)
            registrar(x, y, op, resultado)
        except (KeyError, ValueError):
            resultado = "Erro"

    return render(request, "home.html", {"resultado": resultado})


@csrf_exempt
@require_http_methods(["POST"])
def api_calcular(request):
    """Endpoint JSON consumido pelo frontend em JavaScript."""
    import json

    try:
        dados = json.loads(request.body or b"{}")
    except ValueError:
        return JsonResponse({"erro": "JSON invalido"}, status=400)

    op = str(dados.get("op", "")).strip()
    if op not in OPERACOES:
        return JsonResponse({"erro": "Operacao invalida"}, status=400)

    try:
        x = _converter(dados.get("x"))
        y = _converter(dados.get("y"))
    except ValueError:
        return JsonResponse({"erro": "Numero invalido"}, status=400)

    resultado = aplicar(x, y, op)
    registrar(x, y, op, resultado)

    return JsonResponse(
        {
            "x": x,
            "y": y,
            "op": op,
            "resultado": formatar(resultado),
            "erro": resultado == "Erro",
        }
    )


@require_http_methods(["GET"])
def api_historico(request):
    """Ultimos 10 calculos. Sem banco migrado devolve lista vazia com aviso."""
    try:
        calculos = list(Calculo.objects.order_by("-id")[:10])
        aviso = None
    except Exception:
        calculos, aviso = [], "banco nao inicializado: rode `python manage.py migrate`"

    return JsonResponse(
        {
            "calculos": [
                {
                    "x": c.x,
                    "y": c.y,
                    "operacao": c.operacao,
                    "expressao": "%s %s %s" % (formatar(c.x), c.operacao, formatar(c.y)),
                    "resultado": c.resultado,
                }
                for c in calculos
            ],
            "aviso": aviso,
        }
    )
