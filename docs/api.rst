API
===

*Run a CherryPy wsgi server to serve the application*

.. code-block:: bash

   $ microbe runserver

.. option:: -i, --ip
            
            determine the host to serve the application (default=127.0.0.1)

.. option:: -p, --port
   
            determine the port to serve the application (default=8000)

.. option:: -u, --url

            determine the url to serve the application (default=/)

*Create a Zip file to save Microbe contents and config file*

.. code-block:: bash

   $ microbe save

.. option:: -o, --output

            determine the output Zip file name (default=microbe.zip)

*Restore a Zip file containing contents and config file obtained by ``save`` command*

.. code-block:: bash

   $ microbe restore <archive.zip>

*Create easily a theme skeleton for Microbe*

.. code-block:: bash

   $ microbe theme <theme-name> <author>
   
