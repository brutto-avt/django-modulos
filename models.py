from django.template.loader import render_to_string
from django.db import models

class Pagina(models.Model):
	nome = models.CharField(max_length=100)
	url = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.nome
	
	class Meta:
		ordering = ('url',)

class Modulo(models.Model):
	nome = models.CharField(max_length=100)
	id_css = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.nome
	
	class Meta:
		ordering = ('nome',)
	
class Componente(models.Model):
	nome = models.CharField(max_length=100)
	template = models.CharField(max_length=150)
	
	def __unicode__(self):
		return self.nome
		
	def render(self, context):
		return render_to_string(self.template, context)
	
	class Meta:
		ordering = ('template',)
		
class ComponentePagina(models.Model):
	pagina = models.ForeignKey('Pagina')
	modulo = models.ForeignKey('Modulo')
	componente = models.ForeignKey('Componente')
	ordem = models.IntegerField()
	visitantes = models.BooleanField(default=True)
	usuarios_registrados = models.BooleanField(default=True)
	administradores = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.pagina.nome + ': ' + self.componente.nome
		
	class Meta:
		ordering = ('pagina', 'modulo', 'ordem',)
		verbose_name = 'Gerenciamento de módulo'
		verbose_name_plural = 'Gerenciamentos de módulos'
