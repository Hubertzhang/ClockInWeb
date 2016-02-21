from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from clockin import settings

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=UserManager.normalize_email(email),
            username=username,
            name=name,
            is_admin=False,
            is_active=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        email = 'admin@admin.com'
        name = 'admin'

        user = self.create_user(username, email, name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return '/personal/%u' % self.pk


class List(models.Model):
    title = models.CharField(max_length=50, unique=True)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    persons = models.ManyToManyField(User, blank=True)
