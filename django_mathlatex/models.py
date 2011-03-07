import os
import re
import shutil
import sys
import tempfile
from django.conf import settings
from django.core.files import File
from django.db import models
from hashlib import sha1

_latex_template = r"""
\documentclass[11pt]{article}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{bm}
\pagestyle{empty}
\begin{document}
\begin{equation*}
%s
\end{equation*}
\end{document}
"""

def _hash_chain(content):
	while True:
		h = sha1(content).hexdigest()
		content = content + ' '
		yield h

def squash_formula(formula):
	f = re.sub(r'(\W)\s+(\W|\w)', '\\1\\2',
			re.sub(r'(\w)\s+(\W)', '\\1\\2',
				re.sub(r'(\w)\s+(\w)', '\\1 \\2', formula))).strip()
	return f


class FormulaManager(models.Manager):
	def get_for_formula(self, formula):
		formula = squash_formula(formula)
		hc = _hash_chain(formula)
		h = hc.next()
		while True:
			f = self.get(formula_hash=h)
			if f.formula == formula:
				return f
			h = hc.next()

	def get_or_create_for_formula(self, formula):
		try:
			return self.get_for_formula(formula)
		except Formula.DoesNotExist:
			return self.create(formula=formula)


class Formula(models.Model):
	formula = models.TextField()
	formula_hash = models.CharField(max_length=40, unique=True, db_index=True)
	image = models.ImageField(upload_to=settings.MATHLATEX_IMAGES_DIR)

	objects = FormulaManager()

	def save(self, *args, **kwargs):
		self.formula = squash_formula(self.formula)
		# gen hash
		hc = _hash_chain(self.formula)
		h = hc.next()
		while Formula.objects.filter(formula_hash=h).exists():
			h = hc.next()
		self.formula_hash = h
		self._gen_image()
		return super(Formula, self).save(*args, **kwargs)

	def _gen_image(self):
		workdir = tempfile.gettempdir()
		fd, texfile = tempfile.mkstemp('.tex', 'formula', workdir, True)
		fh = os.fdopen(fd, 'w+')
		fh.write(_latex_template % self.formula)
		fh.close()
		latex_command = 'latex -halt-on-error -output-directory %s %s %s' % \
						(workdir, texfile, '' if settings.DEBUG else '> /dev/null 2>&1')
		retcode = os.system(latex_command)
		if retcode != 0:
			raise ValueError("latex returned code %s for formula:\n%s" % (retcode, self.formula))
		dvifile = texfile.replace('.tex', '.dvi')
		pngfile = texfile.replace('.tex', '.png')
		dvipng_command = 'dvipng -T tight -z 9 -bg Transparent -o %s %s %s' % \
						(pngfile, dvifile, '' if settings.DEBUG else '> /dev/null 2>&1')
		retcode = os.system(dvipng_command)
		if retcode != 0:
			raise ValueError("dvipng returned code %s for formula:\n%s" % (retcode, self.formula))
		self.image.save(os.path.basename(pngfile), File(open(pngfile, 'rb')), save=False)
		os.remove(texfile)
		os.remove(dvifile)
		os.remove(pngfile)
