django_mathlatex
================

Render PNG images of math formulas written in LaTeX notation.
It's simple as hell:

::

    {% load mathlatex %}
    {% math %}
        E = mc^2
    {% endmath %}

Requirements and confirguration
-------------------------------

The required tools are:
    * ``latex`` with ``amsmath`` package,
    * ``dvipng``

The configuration consists of one declaration in ``settings.py``:

::

    MATHLATEX_IMAGES_DIR = 'math/'        # Or wherever you wish under MEDIA_ROOT

Examples
--------

Always include ``{% load mathlatex %}`` in your template.

To simply put a formula inline, write:

::

    <p>
    Einstein said that {% math %}E = mc^2{% endmath %}.
    </p>

    <p>
    We can say more:
    </p>
    {% math %}
                \left\{
                \begin{array}{ll}
                x = ct + x\cos(\omega t)\\
                z = R\sin(\omega t)
                \end{array}
            \right. \Leftrightarrow
            \left\{
                \begin{array}{ll}
                x = \frac{L}{T}t+R\cos(\omega t)\\
                z = R\sin(\omega t)
                \end{array}
            \right. \Leftrightarrow
            \left\{
                \begin{array}{ll}
                x = \frac{\omega t}{k}+R\cos(\omega t)\\
                z = R\sin(\omega t)
                \end{array}
            \right.
    {% endmath %}

You may also obtain the instance of formula's model by assigning it to a value:

::

    {% math as einstein %}E=mc^2{% endmath %}
    <p>
    The following equation illustrates mass-energy equivalence:
    </p>
    <img src="{{ einstein.image.url }}" alt="Mass - energy equivalence" />

Alternatively, you may pass an equation as context variable:

::

    from django.template import Template, Context
    t3 = Template("{% load mathlatex %}{% math %}{{ einstein }}{% endmath %}")
    ctx = Context({'einstein': 'E = mc ^ 2'})

Also you could use math as filter in templates

::
	{{text|math}}
