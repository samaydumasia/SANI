from hashlib import new
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Message
from bot import ask
# Create your views here.

def index(request):
    
    return render(request, 'index.html', {
        'title':'Home'
    })
    

def chat(request):
    return render(request, 'chat.html', {
        'title':'Chat'
    })
    
def login(request):
    
    # if request.method == "POST":        
    #     email=request.POST['email']
    #     password=request.POST['password']
        
    #     user = authenticate(email=email, password=password)
        
    #     if user is not None:
    #         authenticate.login(request, user)
    #         return redirect('/')
    #     else:
    #         messages.info(request, "Credentials invalid")
        
    return render(request, 'login.html', {
        'title':'Login'
    })

    
# def signup(request):
    
#     if request.method == "POST":
#         name=request.POST['name']
#         email=request.POST['email']
#         password=request.POST['password']
        
#         if Signup.objects.filter(email = email).exists():
#             messages.info(request, "Email already exist")
#             return redirect('signup')
#         else:
#             user = Signup.objects.create(name=name, email=email, password=password)
#             user.save()
#             return redirect('login')
        
    return render(request, 'signup.html',  {'title':'Sign up'})
        
def profile(request):
    return render(request, 'profile.html', {
        'title':'Profile'
    })

def send(request):
    
    if request.method == 'POST': 
        username = request.POST.get('username')
        text = request.POST.get('message')  

        new_message = Message.objects.create(text=text, username=username)
        new_message.save()

        x = ask(text)
        
        new_message = Message.objects.create(text=x, username="bot")
        new_message.save()
        
    return HttpResponse(request, x)

def getMessages(request):
    messages = Message.objects.filter()
    
    return JsonResponse({"messages":list(messages.values())})

def analysis(request):
     return render(request, 'analysis.html' )


# def postdata(request):
#     # name = request.POST['name']
#     # new_message = Data.objects.create(name=name)
#     # new_message.save()
#     # print(new_message)
#     name = ''
#     if request.method == 'POST': 
#         name = request.POST.get('name')
#         new_message = Data.objects.create(
#             name=name
#         )
#         new_message.save()        
        
#     return HttpResponse("message sent")
    
    