from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, ForeignKey, CASCADE, CharField, TextField, DateTimeField, TextChoices, FileField, \
    ManyToManyField, SmallIntegerField

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    phone_number = CharField(max_length=20, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    username = None




class Post(Model):
    class StatusChoices(TextChoices):
        new='new','New'
        completed='completed','Completed'
    title=CharField(max_length=255)
    description=TextField()
    file=FileField(upload_to='posts')
    deadline=DateTimeField()
    status=CharField(max_length=50,choices=StatusChoices.choices,default=StatusChoices.new)
    customer=ForeignKey('api.User',CASCADE,related_name='posts')

class Job(Model):
    name = CharField(max_length=255)
    post_subjob = ManyToManyField('api.Post', related_name='post_subjobs', blank=True)

class SubJob(Model):
    name = CharField(max_length=255)
    job_id=ForeignKey('api.Job',on_delete=CASCADE,related_name='subjobs')

class Employee(Model):
    experience=SmallIntegerField()
    lincedin=CharField(max_length=255)
    description=TextField()
    user=ForeignKey('api.User',on_delete=CASCADE,related_name='employees')
    rating=SmallIntegerField()
    cv=FileField(upload_to='employees/cv')
    sub_job=ForeignKey('api.SubJob',on_delete=CASCADE,related_name='employees')


