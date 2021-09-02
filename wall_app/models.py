from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if postData['password_confirm']!=postData['password']:
            errors["password"] = "Las contraseñas deben coincidir"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    email= models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    allowed= models.BooleanField(default =True)
    avatar = models.URLField(
        default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 

    def __repr__(self) -> str:
        return f'{self.id}:{self.name}'
    def __str__(self) -> str:
        return f'{self.id}:{self.name}'

class Mensaje(models.Model):
    texto= models.TextField()
    escritor= models.ForeignKey(User,  related_name="mensajes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self) -> str:
        return f'({self.id}){self.escritor.id} {self.escritor.name}:{self.texto}'

    def __str__(self) -> str:
        return f'({self.id}){self.escritor.id}:{self.texto}'

class Comentario(models.Model):
    texto= models.TextField()
    escritor= models.ForeignKey(User,  related_name="comentarios", on_delete = models.CASCADE)
    mensaje= models.ForeignKey(Mensaje,  related_name="comentarios", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self) -> str:
        return f'({self.id}){self.escritor.id}/{self.mensaje.id}:{self.texto}'
    def __str__(self) -> str:
        return f'({self.id}){self.escritor.id}{self.escritor.name}/{self.mensaje.id}:{self.texto}'