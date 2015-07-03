import os
from django.template import Library, Node, resolve_variable, TemplateSyntaxError
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from modulos.models import Pagina, Modulo, ComponentePagina
from haystack.forms import SearchForm

register = Library()

class ModulosComponentestNode(Node):
	def __init__(self, modulo_id):
		self.modulo_id = modulo_id

	def render(self, context):
		conteudo = ''
		usuario = context['user']
		try:
			pagina = Pagina.objects.get(url=context['request'].path)
			modulo = Modulo.objects.get(id_css=self.modulo_id)
		except:
			conteudo = ''
		componentes = ComponentePagina.objects.filter(pagina=pagina, modulo=modulo)
		if not componentes:
			conteudo = ''
		if usuario.is_authenticated():
			if usuario.is_staff:
				componentes = componentes.filter(administradores=True)
			else:
				componentes = componentes.filter(usuarios_registrados=True)
		else:
			componentes = componentes.filter(visitantes=True)
		if componentes.count > 0:
			componentes = componentes.order_by('ordem')
			for componente in componentes:
				html = componente.componente.render(context).strip(u'\ufeff').strip()
				conteudo += html
		return mark_safe(conteudo)

class SearchBoxNode(Node):
	def render(self, context):
		conteudo = render_to_string('componentes/busca_topo.html', {'search_form': SearchForm()})
		conteudo = conteudo.strip(u'\ufeff').strip()
		return mark_safe(conteudo)

@register.tag
def get_componentes_modulo(parser, token):
	try:
		tag_name, modulo_id = token.split_contents()
	except ValueError:
		raise TemplateSyntaxError("%r tag requires exactly one argument" % token.contents.split()[0])
	return ModulosComponentestNode(modulo_id)
	
@register.tag
def create_search_box(parser, token):
	try:
		tag_name = token.split_contents()
	except ValueError:
		raise TemplateSyntaxError("%r tag requires no arguments" % token.contents.split()[0])
	return SearchBoxNode()