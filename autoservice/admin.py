from django.contrib import admin
from autoservice import models
admin.site.register(models.AS_user)
admin.site.register(models.Car)
admin.site.register(models.UserCar)
admin.site.register(models.Language)

# Register your models here.
