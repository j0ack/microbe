Frequently asked questions
==========================

**How to report a bug**

You can contact me at this address to report a bug or ask a question about Microbe : joachim.trouverie@joacodepel.tk or you can use the `Issue tracker`_.

**Include a media in my content**

To include a file in your contact you need to upload directly in your editor if your browser supports the HTML5 file API or using the :doc:`</media>` management tab in the administration page.

**ReCaptcha keys**

You can enable comments for your posts in the configuration tab in administration page.

To avoid spam, Microbe uses `ReCaptcha`_ service. You can get keys from ReCaptcha website for your site.

**Robots.txt**

You can add a ``robots.txt`` file for your blog. For that you just need to upload it using the :doc:`</media>` management. Unlike the others files ``robots.txt`` will be recheable at ``http:/www.yourwebsite.com/<sub-url/>robots.txt``.

**Sitemaps**

Sitemaps for your blog are auto generated from your contents at ``http:/www.yourwebsite.com/<sub-url/>sitemaps.xml``.

**Favicon**

You can add your own favicon or use the beautiful Microbe's favicon for your application.

*To add your own favicon*

- Copy your favicon file in ``$HOME/.microbe/themes/<your-theme-name>/img/``
- Use the following command to include it in your theme templates

.. code-block:: django
   
   <link rel="icon" type="image/png" href="{{ theme_static('img/favicon.png') }}">

*To use default favicon*

- Just add to your templates the following command

.. code-block:: django

   <link rel="icon" type="image/png" href="{{ url_for('static', filename='img/favicon.png') }}">

.. _Issue tracker: https://github.com/j0ack/microbe/issues/
.. _ReCaptcha: http://www.google.com/recaptcha
