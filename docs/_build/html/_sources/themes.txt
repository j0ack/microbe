Theming support
###############

Microbe comes with two themes ``dark`` and ``clear``. You can switch your website theme using the ``Theme`` tab in administration page.

You can get more themes at the address http://hg.joacodepel.tk/get_microbe/microbe-themes/. Download the last archive including the subrepositories and extract it.

To install a new theme paste the theme directory in ``$HOME/.microbe/themes/``.

How to create my own theme
--------------------------

To create your own theme you can customize the default themes or create a new one from scratch.

Themes are based on `Jinja2 <http://jinja2.pocoo.org/>`_ template engine using the `Flask-Themes2 <http://www.google.com/recaptcha>`_ extension.

Skeletton
+++++++++

First you need to create a theme folder like described::

    mythemedir
    ├── info.json
    ├── static
    │   └── css
    │   └── js
    └── templates
        └── base.html
        └── layout.html
        └── page.html 
        └── index.html 

*info.json*

The ``info.json`` file must contains the theme’s metadata::

    {
        "application": "microbe",
        "identifier": "your_theme_id",
        "name": "your_theme_name",
        "author": "Your name",
        "license": "Your license",
        "description": "A description",
        "version": "your_theme_version",
        "preview": "A preview file stored in static dir if available"
    }

*base.html*

Base template to include your static files in all your views.

You can access your static directory thanks to ``theme_static`` function::

    <!doctype html>
      <head>
        <link rel="stylesheet" src="{{ theme_static('css/style.css') }}">
      </head>
      <body>
      </body>
    </html>

*layout.html*

Layout template extending your base to design your blocks using Jinja2 blocks tag.

You can extend your theme templates using ``theme`` function::

    {% extends theme('base.html') %}

*page.html*

Templates used to render your static pages and posts objects.

*index.html*

Templates used to render a list of objects (used by ``index``, ``archives``, ``tags`` and ``categories``)

Variables
+++++++++

These are the variables you can use in the different templates :

+------------------------------+-----------------------------------------+
| Name                         + Description                             |
+==============================+=========================================+
| *config.SITENAME*            | Site name registered in config          |
+------------------------------+-----------------------------------------+
| *config.SUBTITLE*            | Site description registered in config   |
+------------------------------+-----------------------------------------+
| *config.RSS*                 | ``Y`` if RSS is enabled else ``N``      |
+------------------------------+-----------------------------------------+
| *g.links*                    | Dict of links registered in Admin page  |
|                              | ``{ CATEGORY : [link1, link2] }``       | 
+------------------------------+-----------------------------------------+
| *g.categories*               | List of posts categories                |
+------------------------------+-----------------------------------------+
| *g.search_form*              | Form to search in contents              |
+------------------------------+-----------------------------------------+
| *page*                       | Current content object                  |
|                              |      - ``summary``                      |
|                              |      - ``path``                         |
|                              |      - ``title``                        |
|                              |      - ``comments``                     |
|                              |      - ``published``                    |
|                              |      - ``author``                       |
+------------------------------+-----------------------------------------+


Please refers to themes example to see how use it.

Feel free to create your own theme and contact me for a pull request.
