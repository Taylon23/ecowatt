from django.shortcuts import render


def blog(request):
    return render(request,"blog.html")

def home(request):
    return render(request,'landing-page.html')