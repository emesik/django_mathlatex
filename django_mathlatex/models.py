import re
from hashlib import sha1
from django.conf import settings
from django.db import models

def _hash_chain(content):
	while True:
		h = sha1(content).hexdigest()
		content = content + ' '
		yield h

def squash_formula(formula):
	return re.compile(r'\s([^\\]').sub(' \\1', formula)


class FormulaManager(models.Manager):
	def get_for_formula(self, formula):
		formula = squash_formula(formula)
		hc = _hash_chain(formula)
		h = hc.next()
		while True:
			f = Formula.objects.get(formula_hash=h)
			if f.formula == formula:
				return f
			h = hc.next()


class Formula(models.Model):
	formula = models.TextField()
	formula_hash = models.CharField(max_length=32, unique=True, db_index=True)
	image = models.ImageField(upload_to=settings.MATHLATEX_IMAGES_DIR)

	def save(self, *args, **kwargs):
		self.formula = squash_formula(self.formula)
		# gen hash
		hc = _hash_chain(self.formula)
		h = hc.next()
		while Formula.objects.filter(formula_hash=h).exists():
			h = hc.next()
		self.formula_hash = h
		super(Formula, self).save(*args, **kwargs)
