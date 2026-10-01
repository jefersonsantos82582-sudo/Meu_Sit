# Calculadora

Calculadora simples com **frontend em JavaScript** e **backend em Python
(Django)**. A interface e a matematica da versao original foram preservadas.

## Estrutura

```
manage.py                  comandos do Django
Meu_Sit/                   configuracao do projeto (Python)
  settings.py
  urls.py
  wsgi.py
  asgi.py
calculadora/               aplicacao Python
  views.py                 regra de negocio e endpoints da API
  models.py                historico dos calculos (SQLite)
  admin.py                 historico visivel em /admin
  urls.py
  templates/home.html      pagina servida pelo Django
  static/calculadora/
    app.js                 frontend em JavaScript
    style.css              estilos
requirements.txt
Procfile.txt
runtime.txt
```

## Como rodar

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abra <http://127.0.0.1:8000/>.

Para criar um usuario do admin: `python manage.py createsuperuser` e acesse
<http://127.0.0.1:8000/admin/> — la ficam registrados todos os calculos.

## API

| Metodo | Rota | Descricao |
| --- | --- | --- |
| `POST` | `/api/calcular/` | Recebe `{"x": 2, "y": 3, "op": "*"}` e devolve o resultado |
| `GET` | `/api/historico/` | Ultimos 10 calculos |

Operacoes aceitas em `op`: `+`, `-`, `*`, `/`, `**`. Divisao por zero devolve
`"Erro"`, igual ao comportamento original.

## Frontend

`calculadora/static/calculadora/app.js` e JavaScript puro: intercepta o envio do
formulario, chama a API e atualiza o resultado sem recarregar a pagina. O
formulario tambem funciona sem JavaScript, porque a view `home` continua
tratando o `POST`.

## Testes

```bash
python manage.py test
```
