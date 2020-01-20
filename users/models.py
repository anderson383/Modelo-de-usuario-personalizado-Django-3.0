from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
# Create your models here.

class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, username, email, password, is_staff, is_superuser,**extra_fields):
        '''
        Recibe username, email, ia_staff, is_superuser y campos extras (nombre, edad, etc)
        '''
        if not email:
            raise ValueError("El campo email es obligatorio papu")
        
        #Normaliza el correo electronico resibe como parameto un correo
        email = self.normalize_email(email)
        
        #Instacia del modelo usuario heredado de la clase BaseUserManager
        user = self.model(username=username, email = email,is_staff=is_staff,is_superuser=is_superuser, **extra_fields)
        
        #Guarda la contraseña del usuario
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,username, email, password=None, **extra_fields ):
        return self._create_user(username,email,password,False,False,**extra_fields)
    
    def create_superuser(self,username, email, password=None, **extra_fields):
        return self._create_user(username,email,password,True,True,**extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=50)
    
   
    #Campos necesarios
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def get_short_name(self):
        return self.first_name