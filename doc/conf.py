project = 'Piecewise Polynomial Curves'
author = 'Matthias Geier'
copyright = '2018, ' + author

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'nbsphinx',
    'sphinxcontrib.bibtex',
]

highlight_language = 'none'
html_sourcelink_suffix = ''

intersphinx_mapping = {'https://docs.python.org/': None}

master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']
pygments_style = 'sphinx'

nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]


def if_docname(text):
    return """
{% set docname = env.doc2path(env.docname, base=None) %}
{% if docname not in [
    'index.ipynb',
    'catmull-rom.ipynb',
] %}
{% set docname = 'doc/' + docname %}
{% set latex_href = ''.join([
    '\href{https://github.com/AudioSceneDescriptionFormat/splines/blob/',
    env.config.release,
    '/',
    docname | escape_latex,
    '}{\sphinxcode{\sphinxupquote{',
    docname | escape_latex,
    '}}}',
]) %}
""" + text + """
{% endif %}
"""


nbsphinx_prolog = if_docname(r"""
.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::

        This page was generated from `{{ docname }}`__.
        Interactive online version:
        :raw-html:`<a href="https://mybinder.org/v2/gh/AudioSceneDescriptionFormat/splines/{{ env.config.release }}?filepath={{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>`

    __ https://github.com/AudioSceneDescriptionFormat/splines/blob/
        {{ env.config.release }}/{{ docname }}

.. raw:: latex

    \nbsphinxstartnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{The following section was generated from {{ latex_href }}
    \dotfill}}
""")

nbsphinx_epilog = if_docname(r"""
.. raw:: latex

    \nbsphinxstopnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{\dotfill\ {{ latex_href }} ends here.}}
""")

# -- Work-around to get LaTeX References at the same place as HTML --------

# See https://github.com/mcmtroffaes/sphinxcontrib-bibtex/issues/156

import docutils
import sphinx.builders.latex

class DummyTransform(docutils.transforms.Transform):

    default_priority = 0

    def apply(self):
        pass

sphinx.builders.latex.BibliographyTransform = DummyTransform

# -- Get version information and date from Git ----------------------------

try:
    from subprocess import check_output
    release = check_output(['git', 'describe', '--tags', '--always'])
    release = release.decode().strip()
    today = check_output(['git', 'show', '-s', '--format=%ad', '--date=short'])
    today = today.decode().strip()
except Exception:
    release = '<unknown>'
    today = '<unknown date>'

# -- Options for HTML output -------------------------------------------------

html_title = project + ', version ' + release
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
}
html_domain_indices = False
html_show_sourcelink = True

mathjax_config = {
    'TeX': {'equationNumbers': {'autoNumber': 'AMS', 'useLabelIds': True}},
}

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'printindex': '',
    'sphinxsetup': r"""
        VerbatimColor={HTML}{F5F5F5},
        VerbatimBorderColor={HTML}{E0E0E0},
        noteBorderColor={HTML}{E0E0E0},
        noteborder=1.5pt,
        warningBorderColor={HTML}{E0E0E0},
        warningborder=1.5pt,
        warningBgColor={HTML}{FBFBFB},
    """,
    'preamble': r"""
\usepackage[sc,osf]{mathpazo}
\linespread{1.05}  % see http://www.tug.dk/FontCatalogue/urwpalladio/
\renewcommand{\sfdefault}{pplj}  % Palatino instead of sans serif
\IfFileExists{zlmtt.sty}{
    \usepackage[light,scaled=1.05]{zlmtt}  % light typewriter font from lmodern
}{
    \renewcommand{\ttdefault}{lmtt}  % typewriter font from lmodern
}
""",
}

latex_show_urls = 'footnote'
latex_domain_indices = False

latex_documents = [
    (master_doc, 'PiecewisePolynomialCurves.tex', project, author, 'howto'),
]

latex_additional_files = ['references.bib']

# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
