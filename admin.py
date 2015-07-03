from django.contrib import admin
from models import Pagina, Modulo, Componente, ComponentePagina
from django.contrib.admin.options import ModelAdmin

class AdminComponentePagina(ModelAdmin):
	list_display = ('pagina', 'modulo', 'componente', 'ordem',)

admin.site.register(Pagina)
admin.site.register(Modulo)
admin.site.register(Componente)
admin.site.register(ComponentePagina, AdminComponentePagina)