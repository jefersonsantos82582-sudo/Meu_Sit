from django.shortcuts import render

def home(request):
    resultado = None

    if request.method == "POST":
        x = float(request.POST["x"])
        y = float(request.POST["y"])
        op = request.POST["op"]

        if op == "+":
            resultado = x + y
        elif op == "-":
            resultado = x - y
        elif op == "*":
            resultado = x * y
        elif op == "/":
            resultado = x / y if y != 0 else "Erro"
        elif op == "**":
            resultado = x ** y

    return render(request, "home.html", {"resultado": resultado})