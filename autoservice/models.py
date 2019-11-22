from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=255)
    short_code = models.CharField(max_length=3,
                                  default='')
    def __str__(self):
        return self.name +' '+ self.short_code



class Car(models.Model):
    name_ru = models.CharField(default='',
                               max_length=1000)
    name_en = models.CharField(default='',
                               max_length=1000)
    year = models.IntegerField(verbose_name='Год создания')
    date_added  = models.DateTimeField(verbose_name='Дата добавления в систему',
                                      auto_now_add=True,
                                      editable=False)
    def __str__(self):
        return self.name_ru


class AS_user(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    lang = models.ForeignKey(Language,
                             on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email

class UserCar(models.Model):
    user = models.ForeignKey(AS_user,
                             related_name='Владелец',
                             on_delete=models.CASCADE)
    car = models.ForeignKey(Car,
                            related_name='Машина',
                            on_delete=models.CASCADE)
    rent_user = models.ForeignKey(AS_user,
                             related_name='Арендующий',
                                  blank=True,
                                  null=True,
                             on_delete=models.CASCADE)
    already_leased  =models.BooleanField(default=False,
                                         verbose_name='Сдана')
    in_rent  =models.BooleanField(default=False,
                                  verbose_name='Готова к аренде')


# Create your models here.
