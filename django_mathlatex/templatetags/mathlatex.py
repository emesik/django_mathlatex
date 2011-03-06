from django import template
from django.conf import settings
from .. import models

register = template.Library()

class MathLatexNode(template.Node):
	def __init__(self, nodelist, varname=None):
		self.nodelist = nodelist
		self.varname = varname

	def render(self, context):
		content = self.nodelist.render(context)
		f = models.Formula.objects.get_or_create_for_formula(content)
		if self.varname:
			context[self.varname] = f
			return u''
		else:
			return u'<img src="%s" alt="%s" />' % (f.image.url, content)


@register.tag('math')
def do_mathlatex(parser, token):
	nodelist = parser.parse(('endmath',))
	parser.delete_first_token()
	bits = token.split_contents()
	if len(bits) == 1:
		return MathLatexNode(nodelist)
	elif len(bits) == 3 and bits[1] == 'as':
		return MathLatexNode(nodelist, bits[2])
	raise template.TemplateSyntaxError(
			"%s tag syntax is {%% %s [as <variable_name>] %%}" % (bits[0], bits[0]))
