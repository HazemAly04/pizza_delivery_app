from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        extra_fields.setdefault('username', email)  # Set username to email

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Size(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.size}'

class Crust(models.Model):
    id = models.AutoField(primary_key=True)
    crust = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.crust}'

class Sauce(models.Model):
    id = models.AutoField(primary_key=True)
    sauce = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.sauce}'

class Cheese(models.Model):
    id = models.AutoField(primary_key=True)
    cheese = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.cheese}' 

class Pizza(models.Model):
    id = models.AutoField(primary_key=True)

    pepperoni = models.BooleanField(default=False)
    chicken = models.BooleanField(default=False)
    ham = models.BooleanField(default=False)
    pineapple = models.BooleanField(default=False)
    peppers = models.BooleanField(default=False)
    mushrooms = models.BooleanField(default=False)
    onions = models.BooleanField(default=False)
    olives = models.BooleanField(default=False)

    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    sauce = models.ForeignKey(Sauce, on_delete=models.CASCADE)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)

    def get_toppings(self):
        toppings = []
        if self.pepperoni:
            toppings.append('pepperoni')
        if self.chicken:
            toppings.append('chicken')
        if self.ham:
            toppings.append('ham')
        if self.pineapple:
            toppings.append('pineapple')
        if self.peppers:
            toppings.append('peppers')
        if self.mushrooms:  
            toppings.append('mushrooms')
        if self.onions:
            toppings.append('onions')
        if self.olives:
            toppings.append('olives')
        return ', '.join(toppings)
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    eircode = models.CharField(max_length=7)

    name_on_card = models.CharField(max_length=100)
    card = models.IntegerField()
    cvv = models.IntegerField()
    expiry = models.CharField(max_length=5)



class PizzaUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    time_ordered = models.DateTimeField(auto_now_add=True)

