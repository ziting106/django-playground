from django.shortcuts import render

def hello_world(request):
    return render(request, "practices/practices.html")

def greeting(request):
    name = "Jenny"
    return render(request, "practices/greeting.html", {"name": name})