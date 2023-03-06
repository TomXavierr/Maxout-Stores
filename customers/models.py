from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username , password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email    =self.normalize_email(email),
            username =username,
          )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username , password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            
        )
        user.is_admin       = True
        user.is_staff       = True
        user.is_verified    =True
        user.is_superuser   = True
        user.save(using=self._db)
        return user
    

class Account(AbstractBaseUser):
    
    email               = models.EmailField(verbose_name="email",max_length=60,unique=True)
    username            = models.CharField(max_length=30,unique=True)
    date_joined         = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_blocked          = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_verified         = models.BooleanField(default=False)
    hide_email          = models.BooleanField(default=True)
    profile_image       = models.ImageField(upload_to='photos/',null=True , blank=False)
    
    objects = MyAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']
    
    def __str__(self) -> str:
        return self.email
    
    def has_perm(self,perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
    
class Addresses(models.Model):
    first_name                 = models.CharField(max_length=30,null=False,blank=False)
    last_name                  = models.CharField(max_length=30,null=False,blank=False)
    house_name                 = models.CharField(max_length=30,null=False,blank=False)
    street_name                = models.CharField(max_length=30,null=False,blank=False)
    city                       = models.CharField(max_length=30,null=False,blank=False)
    district                   = models.CharField(max_length=30,null=False,blank=False)
    state                      = models.CharField(max_length=30,null=False,blank=False)
    pincode                    = models.BigIntegerField(null=False,blank=False)      
    mobile                     = models.BigIntegerField(null=False,blank=False)
    user_id                    = models.ForeignKey("Account", on_delete=models.CASCADE, default=False , null=False)
    is_primary                 = models.BooleanField(default=False)