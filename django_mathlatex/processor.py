import os
import sys
import shutil
import tempfile
from django.core.files import File
from . import models

_latex_template = """
\documentclass{article}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{bm}
\pagestyle{empty}
\begin{document}
%s
\end{document}
"""

def gen_image(formula):
	workdir = tempfile.gettempdir()
	fd, texfile = tempfile.mkstemp('.tex', 'formula', workdir, True)
	fh = os.fdopen(fd, 'w+')
	fh.write(_latex_template % formula)
	fh.close()
	latex_command = 'latex -halt-on-error -output-directory %s %s' % \
					(workdir, texfile)
	retcode = os.system(latex_command)
	if retcode != 0:
		raise ValueError("latex returned code %s for formula:\n%s" % (retcode, formula))
	dvifile = texfile.replace('.tex', '.dvi')
	pngfile = texfile.replace('.tex', '.png')
	dvipng_command = "dvipng -T tight -z 9 -bg Transparent -o %s %s" % (pngfile, dvifile)
	retcode = os.system(latex_command)
	if retcode != 0:
		raise ValueError("dvipng returned code %s for formula:\n%s" % (retcode, formula))
	png = File(open(pngfile, 'rb'))
	formula = models.Formula()
	formula.image.storage.save(os.path.basename(pngfile), png)
	formula.save()
	shutil.rmtree(workdir)
