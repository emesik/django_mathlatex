from django.template import Template, Context
from django.test import TestCase
from . import models

class SimpleTest(TestCase):
	def test_rendering(self):
		t1 = Template("{% load mathlatex %}{% math %}E = mc^2{% endmath %}")
		t2 = Template("{% load mathlatex %}{% math as einstein %}E = mc^2{% endmath %}{{ einstein.image.url }}")
		ctx = Context({})
		t1.render(ctx)
		t2.render(ctx)
		self.assertEqual(1, models.Formula.objects.count())
