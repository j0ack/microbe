Administrate Microbe
####################

Once you have deploy it successfully you can access your application  at `www.yourwebsite.com`.


.. figure:: ./default.png
    :width: 400px
    :align: center


You can access the administration part using the link at the bottom of the page or entering the following link in your address bar `www.yourwebsite.com/admin/`.

The administration part is protected by a basic access authentication using a user name and a password.

The default account is `admin/microbe`.

.. figure:: ./admin.png
   :width: 400px
   :align: center 


.. warning:: It is recommended to change this password or delete this user after your first connection using the :ref:`users-management`.

.. _users-management:

Users management
================



.. figure:: ./users.png
   :width: 400px
   :align: center


Users management can be accessed using the link `Users` in the administration navigation bar.

You can create/delete/edit users from this interface using the icons placed at the right of the user name.



.. figure:: ./user_edit.png
   :width: 400px
   :align: center

.. note:: Deletion is only permitted if there is at least two users.


Configuration
=============



.. figure:: ./config.png
   :width: 400px
   :align: center


Configuration can be accessed using the link `Configuration` in the administration navigation bar.

+------------------------------+------------------------------------------------+
| Name                         + Description                                    |
+==============================+================================================+
| *Server name*                | Is used by the app to construct the urls       |
+------------------------------+------------------------------------------------+
| *Site name*                  | Site name                                      |
+------------------------------+------------------------------------------------+
| *Site subtitle*              | Site description                               |
+------------------------------+------------------------------------------------+
| *Language*                   | Interface language                             |
+------------------------------+------------------------------------------------+
| *Pagination*                 | Number of entries per page                     |
+------------------------------+------------------------------------------------+
| *Summary length*             | Number of letters in content summary           |
+------------------------------+------------------------------------------------+
| *Comments*                   | Enable or disable comments on posts            |
+------------------------------+------------------------------------------------+
| *Atom feeds*                 | Generate atom feeds or not                     |
+------------------------------+------------------------------------------------+
| Recaptcha public key         | Recaptcha public key to avoid spam on comments |
+------------------------------+------------------------------------------------+
| Recaptcha private key        | Recaptcha private key                          |
+------------------------------+------------------------------------------------+

Contents
========



.. figure:: ./contents.png
   :width: 400px
   :align: center


Contents management can be accessed using the link `Contents` in the administration navigation bar.

You can create/delete/edit contents from this interface using the icons placed at the right column.


.. figure:: ./content_edit.png
   :width: 400px
   :align: center



+------------------------------+------------------------------------------------+
| Name                         + Description                                    |
+==============================+================================================+
| *Title*                      | Content title                                  |
+------------------------------+------------------------------------------------+
| *Category*                   | Content category (unique)                      |
+------------------------------+------------------------------------------------+
| *Tags*                       | Content tags separated by commas               |
+------------------------------+------------------------------------------------+
| *Content*                    | Content using Markdown format                  |
+------------------------------+------------------------------------------------+

Once content has been created or modified, you need to publish it using the icon placed at the right column to make it available on your site.

Media
=====

To use media in your contents you need to upload it first on your server.

You can use the media management accessible using the link `Media` in the administration navigation bar.


.. figure:: ./media.png
   :width: 400px
   :align: center



Upload is managed using the HTML5 file API for the Drag and drop. If your browser doesn't allow it you can use a the regular upload button.


.. figure:: ./media_regular.png
   :width: 400px
   :align: center



Files uploaded will be reachable at `http://www.yourwebsite.com/static/media/<your_file_name>`.

Themes
======

You can choose your theme using the link `Themes` in the administration navigation bar.

You just need to select the theme you want from those displayed


.. figure:: ./themes.png
   :width: 400px
   :align: center



.. note:: For more information about themes, see Theming_support_ part.

Links
=====



.. figure:: ./links.png
   :width: 400px
   :align: center

Links management can be accessed using the link `Links` in the administration navigation bar.


You can create and delete links from this interface using the icons placed at the right.


.. figure:: ./link_edit.png
   :width: 400px
   :align: center


Comments
========

You can enable comments on posts using the `Configuration` menu.

To protect your post, Microbe uses Recaptcha keys to avoid spam (see FAQ_ for more info).

Once you have enabled it, people will be able to add comment using form from your pages.

.. figure:: ./add_comment.png     
        :width: 400px
        :align: center

Avatar for comments are automatically generated from its author using `VizHash.js <https://github.com/sametmax/VizHash.js>`_

It is possible then to moderate comments using the link present in `Content management`.

.. figure:: ./content_comment.png 
        :width: 400px           
        :align: center


.. Links
.. _Theming_support : ./themes
.. _FAQ : ./faq
