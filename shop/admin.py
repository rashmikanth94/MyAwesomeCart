from django.contrib import admin
from . models import product, Contact, Orders, Orderupdate
# Register your models here.
admin.site.register(product)

admin.site.register(Contact)

admin.site.register(Orders)

admin.site.register(Orderupdate)