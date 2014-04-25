Deploy Microbe
##############

Run Microbe
===========

Microbe comes with a command to launch a `CherryPy <http://cherrypy.org/>`_ server to serve the application:: 

    $ microbe --ip 127.0.0.1 --port 80

That's it you can now access your application at ``http://localhost/``.

To access your application from internet you need to configure your router and launch the application with the following parameters::

    $ microbe --ip 0.0.0.0 --port 80

Run in background
-----------------

Microbe does not come with something build for this. You have several solutions.

**Shell background process**

Just use the above command in a shell background process::

    $ nohup microbe --ip 127.0.0.1 --port 80 > microbe.log &

Or run it in a ``screen``.

**Supervisor**

`Supervisor <https://pypi.python.org/pypi/supervisor>`_ is a program allowing you to manage processes. 

Create a configuration file in ``/etc/supervisor/conf.d/`` named ``microbe.conf``::

    [program:microbe]
    command=microbe --ip 127.0.0.1 --port 80
    directory=/path/to/microbe/
    environment=HOME='/your_home/'
    autostart=true
    autorestart=true

Then you need to enable your config file using as root::

    supervisorctl update && supervisorctl microbe start    


Deploy Microbe
==============

Apache setup
------------

The modern Web Python servers all work the same way, following an norm for interfacing: WSGI.

This is the most effective solution, and the best to use. But it will require the setup of the Apache module mod_wsgi.

First enable mod_wsgi::

    $ a2enmod wsgi

Then create an Apache configuration file, usually in ``/etc/apache/sites-available/``. Name it microbe::

    <VirtualHost *:80>
        ServerName www.yourwebsite.com

        WSGIDaemonProcess microbe user=www-data group=www-data processes=1 threads=5
        WSGIScriptAlias / /path/to/microbe/app.wsgi

        <Directory /path/to/microbe/microbe/>
            WSGIProcessGroup microbe
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

Activate the website::

    $ a2ensite microbe

And reload Apache configuration::

    service apache2 reload

You.ll note that we refer to a file named app.wsgi. It.s a Python file creating the application Apache is going to use to start the Python process::

    import os, sys

    MICROBE_PARENT_DIR = '/path/to/microbe/parent/dir'
    sys.path.insert(0, MICROBE_PARENT_DIR)

    from microbe.views import run_server
    run_server(port=your_port, ip=your_ip)

Nginx setup
-----------

Whereas Apache, Nginx doesn't run any Python process, it only serve requests from outside to the Python server.

Therefore there are two steps:

- Run the python process
- Run Nginx

**Python process**

As described in Getting_started_ part, Microbe comes a command to run the server. This time we will point to another port to use Nginx proxy module::

    $ microbe --ip 127.0.0.1 -- port 8000

**Nginx**

Create a configuration file in ``/etc/nginx/sites-available/`` named ``microbe``.

The minimal configuration file to run the app is::

    server {
            listen 80;
            server_name www.yourwebsite.com

            location /static/ {
                root /path/to/microbe/microbe/static/;
            }

            location / {
                    proxy_pass http://127.0.0.1:8000;
                    proxy_set_header Host $http_host;
            }
    }

You can make some adjustements to get a better user experience::

    server {
            listen 80;
            server_name www.yourwebsite.com
            
            location /static/ {
                    root /path/to/microbe/microbe/static/;
                    gzip  on;
                    gzip_http_version 1.0;
                    gzip_vary on;
                    gzip_comp_level 6;
                    gzip_proxied any;
                    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
                    gzip_buffers 16 8k;
                    # Disable gzip for certain browsers.
                    gzip_disable ~@~\MSIE [1-6].(?!.*SV1)~@~];
                    expires modified +90d;
            }

            location / {
                    proxy_pass 127.0.0.1:8000;
                    proxy_set_header Host $http_host;
            }

    }

Create a symbolic link to enable the new configuration and restart the Nginx service::

    ln -s /etc/nginx/sites-available/microbe /etc/nginx/sites-enabled
    service nginx restart

.. Links
.. _Getting_started : ./getting_started
