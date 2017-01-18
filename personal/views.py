from django.shortcuts import render

def index(request):
    return render(request, 'personal/home.html')

def contact(request):
    content = [
        'Hello, that is my contact page',
        'Contact me if you can'
    ]
    return render(request, 'personal/basic.html', {'content': content})
