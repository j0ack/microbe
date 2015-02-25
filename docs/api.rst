API
===

**Runserver**

.. code-block:: bash

   $ microbe runserver [-i 127.0.0.1] [-p 8000] [-u /]

..

    Run a CherryPy wsgi server to serve the application

    .. option:: -i, --ip
            
                determine the host to serve the application (default=127.0.0.1)

    .. option:: -p, --port
                   
                determine the port to serve the application (default=8000)

    .. option:: -u, --url

                determine the url to serve the application (default=/)


**Save**

.. code-block:: bash

   $ microbe save [-o microbe.zip]

..

    Create a Zip file to save Microbe contents and config file

    .. option:: -o, --output

                determine the output Zip file name (default=microbe.zip)

**Restore**

.. code-block:: bash

   $ microbe restore <archive.zip>

..

    Restore a Zip file containing contents and config file obtained by ``save`` command 

    **Paramaters**:
    
    - ``archive.zip`` : Input zip file name containing backup for microbe generated with ``save``

**Theme**

.. code-block:: bash

   $ microbe theme <theme-name> <author>

..
 
    Create easily a theme skeleton for Microbe 

    **Parameters**:

    - ``theme-name`` : The new theme's name
    - ``author`` : Your name, this will be used in the theme's ``info.json``
