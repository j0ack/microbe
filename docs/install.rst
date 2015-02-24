Getting started
===============

Install Microbe
---------------

You need to have Python installed on your server to use Microbe. The install script will download for you all the dependencies.

With pip
^^^^^^^^

If you already have ``pip`` installed on your server you can use it to install Microbe

.. code-block:: bash

   $ pip install microbe


It will download Microbe from `Pypi`_

Without pip
^^^^^^^^^^^

You can install ``pip`` easily using your package manager or install Microbe manually following these steps :

1. Get the last archive of `Microbe`_
2. Extract it
3. Change path to extracted archive
4. Run ``python setup.py install``

.. note::
   Keep in mind that OS will otfen require you to prefix the above commands with ``sudo`` in order to install the app system-wide.
   It is recommended to create a virtual environment for Microbe via `virtualenv`_


Upgrade Microbe
---------------

.. warning::
   Upgrading Microbe will delete all the files contained in the application folder including your contents and the config file saved.

To preserve your contents, Microbe comes with two :doc:`commands /api` : ``save`` and ``restore``.

1. Save your contents in a Zip file using the ``save`` command
2. Upgrade Microbe with or without ``pip``
3. Restore your contents using the ``restore`` command

With pip
^^^^^^^^

.. code-block:: bash
   
   $ microbe save -o mymicrobe.zip
   $ pip install --upgrade microbe
   $ microbe restore mymicrobe.zip

Without pip
^^^^^^^^^^^

.. code-block:: bash

   $ microbe save -o mymicrobe.zip
   $ cd /path/to/microbe/folder/
   $ python setup.py develop -u
   $ cd -
   $ wget https://github.com/j0ack/microbe/archive/master.zip
   $ unzip master.zip
   $ cd master
   $ python setup.py install
   $ cd ..
   $ microbe restore mymicrobe.zip

   
.. _Pypi: http://pypi.python.org
.. _Microbe: https://github.com/j0ack/microbe/archive/master.zip
.. _virtualenv: http://www.virtualenv.org/
