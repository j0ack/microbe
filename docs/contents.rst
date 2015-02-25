Contents management
===================

.. note::
   You need to be logged in to the Microbe administration part to manage users, for more information see :doc:`/administrate`.


Contents
--------

Contents management can be accessed using the link ``Contents`` in the administration navigation bar or following this link : ``www.yourwebsite.com/<sub-url/>admin/contents``.

.. image:: _static/contents.png
   :align: center
   :class: screenshot

This page lists all the contents saved in the application

.. image:: _static/content_edit.png
   :align: center
   :class: screenshot

You can create/delete/edit/publish contents and from this interface using the icons placed at the right column.

+------------------------------+-----------------------------------------------+
| Name                         | Description                                   |
+==============================+===============================================+
| *Title*                      | Content title                                 |
+------------------------------+-----------------------------------------------+
| *Category*                   | Content category (unique)                     |
+------------------------------+-----------------------------------------------+
| *Tags*                       | Content tags separated by commas              |
+------------------------------+-----------------------------------------------+
| *Content*                    | Content using Markdown format                 |
+------------------------------+-----------------------------------------------+


Once content has been created or modified, you need to publish it using the icon placed at the right column to make it available on your site.

Comments
--------

You can enable comments on posts using the :doc:`/config`.

To protect your post, Microbe uses ReCaptcha keys to avoid spam (see :doc:`/faq` for more info).

Once you have enabled it, people will be able to add comment using form from your pages.

.. image:: _static/comment.png
   :align: center
   :class: screenshot

Avatar for comments are automatically generated from its author using `VizHash.js`_.

It is possible then to moderate comments using the link present in ``Content management``.


.. image:: _static/content_comment.png
   :align: center
   :class: screenshot

.. _VizHash.js: https://github.com/sametmax/VizHash.js
