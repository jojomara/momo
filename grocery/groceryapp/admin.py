from django.contrib import admin # type: ignore
from . models import *


admin.site.register(stockx)
class StockxAdmin(admin.ModelAdmin):
    list_display = ('item', 'other_fields')

admin.site.register(Product)

