Frequently asked questions
##########################

How to report a bug
===================

You can contact me at this address to report a bug or ask a question about Microbe : joachim.trouverie@joacodepel.tk

Include a media in my content
=============================

To include a file in your contact you need to upload it first on your server using the Media_management_ tab in the administration page.

How to include code blocks
==========================

Microbe use the `CodeHilite` Markdown extension to generate code blocks. 

You can find a documentation for this extension `here <https://pythonhosted.org/Markdown/extensions/code_hilite.html>`_.

I made an error in config
=========================

Microbe come with a commnd to reinit the config file in case you made a mistake::
        
        $ microbe reinit

.. warning:: Your configuration file will be removed, this can not be undoned

ReCaptcha keys
==============

You can enable comments for your posts in the configuration tab in administration page. 

To avoid spam, Microbe use `ReCaptcha <http://www.google.com/recaptcha>`_ service. You can get keys from ReCaptcha website for your site.

Robots.txt
==========

You can add a ``robots.txt`` file for your blog. For that you just need to upload it using the Media_management_. Whereas the others files ``robots.txt`` will be recheable at ``http:/www.yourwebsite.com/<sub-url/>robots.txt``.

Sitemaps
========

Sitemaps for your blog are auto generated from your contents at ``http:/www.yourwebsite.com/<sub-url/>sitemaps.xml``.

Favicon
=======

You can add your own favicon or use the beautiful Microbe favicon for your application.

To add your own favicon
-----------------------
- Copy your favicon file in ``$HOME/.microbe/themes/<your-theme-name>/img/``
- Use the following command to include it in your theme templates::
    
    <link rel="icon" type="image/png" href="{{ theme_static('img/favicon.png') }}">

To use default favicon
----------------------
- Just add to your templates the following command::
    
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='img/favicon.png') }}">

.. Links
.. _Media_management : ./media
