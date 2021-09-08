from django.shortcuts import render, HttpResponse,redirect
from .decorators import login_required
from django.db import IntegrityError
from .models import  Comentario, Mensaje, User
from django.contrib import messages
import bcrypt

@login_required
def index(request):
    logout='Logout'
    mensajes=Mensaje.objects.all().order_by('-created_at')
    context = {
        "logout":logout,
        "mensajes":mensajes
    }
    return render(request, 'index.html', context)


def register(request):
    if request.method == "GET":
        context={}
        return render(request, 'register.html', context)
    if request.method == "POST":
        name=request.POST['name']
        email =request.POST['email']
        password=request.POST['password']
        #password_confirm= request.POST['email']

        errors= User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for k, mensaje_de_error in errors.items():
                messages.error(request,mensaje_de_error)
        
        else:
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            try:
                user=User.objects.create(name=name,email=email,password=pw_hash)
                request.session['user']={
                    'id':user.id,
                    'name':user.name,
                    'email':user.email,
                    'avatar':user.avatar
                }
                return redirect('/wall')
            except IntegrityError :
                messages.error(request,'Este correo ya tiene un usuario.')
                return redirect('/register')

def login(request):
    email = request.POST['email']
    password=request.POST['password']
    try:
        user= User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request,'Usuario inexistente o contraseña incorrecta')
        return redirect('/register')

    if not bcrypt.checkpw(password.encode(),user.password.encode()):
        messages.error(request,'Usuario inexistente o contraseña incorrecta')
        return redirect('/register')

    request.session['user']={
        'id':user.id,
        'name':user.name,
        'email':user.email,
        'avatar':user.avatar
    }
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/register')

def message_new(request):

    usuario_id=request.session['user']['id']
    mensaje=request.POST['mensaje']
    escritor=User.objects.get(id=usuario_id)
    Mensaje.objects.create(texto=mensaje,escritor=escritor)
    if 'from' in request.POST:
        return redirect('/'+request.POST['from'])
    return redirect('/index')

def message_edit(request,msg_id):
    mensaje_t=Mensaje.objects.get(id=msg_id)
    mensaje_t.texto=request.POST['texto']
    print(f'id:{msg_id},m:{mensaje_t.texto}')
    mensaje_t.save()
    messages.success(request,'Mensaje modificado con exito.')
    return redirect('/wall')

#aca van los mensajes con sus comentarios
def wall(request):
    mensajes=Mensaje.objects.all().order_by('-created_at')
    context = {        
        "mensajes":mensajes
    }
    return render(request, 'wall.html', context)

    
def comentario_new(request):
    usuario_id=request.session['user']['id']
    mensaje_id=request.POST['mensaje_id']
    comentario=request.POST['comentario']
    escritor=User.objects.get(id=usuario_id)
    msg=Mensaje.objects.get(id=mensaje_id)
    Comentario.objects.create(texto=comentario,escritor=escritor,mensaje=msg)
    return redirect('/wall')

def comentario_edit(request,cmt_id):
    target=Comentario.objects.get(id=cmt_id)
    target.texto=request.POST['texto']
    print(f'id:{cmt_id},m:{target.texto}')
    target.save()
    messages.success(request,'Comentario modificado con exito.')
    return redirect('/wall')

def comentario_destroy(request,cmt_id):
    target=Comentario.objects.get(id=cmt_id)
    target.delete()
    messages.success(request,'Comentario eliminado con exito.')
    return redirect('/wall')

def message_destroy(request,msg_id):
    target=Mensaje.objects.get(id=msg_id)
    target.delete()
    messages.success(request,'Mensaje eliminado con exito.')
    return redirect('/wall')