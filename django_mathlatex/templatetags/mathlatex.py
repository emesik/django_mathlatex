from django import template
from .. import models
from .. import processor

register = template.Library()

class MathLatexNode(template.Node):
	def __init__(self, nodelist, varname=None):
		self.nodelist = nodelist
		self.varname = varname

	def render(self, context):
		content = self.nodelist.render(context)


@register.tag('mathlatex')
def do_mathlatex(parser, token):
	nodelist = parser.parse(('endmathlatex',))
	parser.delete_first_token()
	bits = token.split_contents()
	if len(bits) != 1:
		return MathLatexNode(nodelist)
	elif len(bits) == 3 and bits[1] == 'as':
		return MathLatexNode(nodelist, bits[2])
	raise template.TemplateSyntaxError(
			"%r tag syntax is {%% %r [as <variable_name>] %%}" % (bits[0], bits[0]))
