Deploy Microbe
==============

Microbe is a `Flask`_ application which is served by the `CherryPy`_ WSGI container.

Launch on port 80
-----------------

.. note::
   On Unix systems ports below to 1024 are reserved to processes run by root

CherryPy stands on its own, but as an application server, it is often located in shared or complex environments.

If it is not your case you can deploy Microbe launching it with the following parameters as a :doc:`daemon </run>`.

.. code-block:: bash

   $ microbe runserver --ip 0.0.0.0 --port 80


.. note::
   The ip set to ``0.0.0.0`` allows users to access your website from outside.

Reverse proxy
-------------

It is not uncommon to run CherryPy behind a reverse proxy if you already have a web server installed preventing you to use port 80.

First you need to run Microbe as a :doc:`daemon </run>`..

Here's for example a simple `Nginx`_ configuration which proxies to an application served on localhost at port 8000. You can easily adapt it to your needs.

.. code-block:: nginx

   server {
       listen 80;
       server_name www.yourwebsite.com

       location </your-sub-url>/static/ {
           alias /path/to/microbe/microbe/static/;
       }

       location </your-sub-url>/ {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $http_host;
       }
   }

You can make some adjustments to get a better user experience

.. code-block:: nginx

   server {
       listen 80;
       server_name www.yourwebsite.com

       location </your-sub-url>/static/ {
           alias /path/to/microbe/microbe/static/;
           gzip  on;
           gzip_http_version 1.0;
           gzip_vary on;
           gzip_comp_level 6;
           gzip_proxied any;
           gzip_buffers 16 8k;
           gzip_disable ~@~\MSIE [1-6].(?!.*SV1)~@~];
           expires modified +90d;
       }

       location </your-sub-url>/ {
           proxy_pass 127.0.0.1:8000;
           proxy_set_header Host $http_host;
       }

   }

                
.. _Flask: http://flask.pocoo.org/
.. _CherryPy: http://cherrypy.org/
.. _Nginx: http://nginx.org
                                                                                                                                                                                                                                                              
