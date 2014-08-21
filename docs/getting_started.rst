Getting started
###############

Installing Microbe
==================

If you already use Pip
----------------------

Just type::
        
    pip install microbe


If Pip is not installed
-----------------------

- Get the last archive `here <https://gitorious.org/get_microbe/microbe/archive/master.tar.gz>`_
- Extract all of it where you whish the site to be stored
- Go to the extracted files
- ``python setup.py install``

Virtualenv note
---------------

Keep in mind that OS will otfen require you to prefix the above commands with ``sudo`` in order to install the app system-wide.

It is recommended to create a virtual environment for Microbe via `virtualenv <http://www.virtualenv.org/>`_ ::

    $ mkdir $HOME/site
    $ cd $HOME/site
    $ virtualenv venv
    $ source venv/bin/activate

Then install the app using one of the methods described above.

Upgrading
=========

First you need to save your contents before upgrading the application. Copy the files contained in the ``content`` placed at your application root::

    find microbe_root_dir -name 'content' -exec cp -r '{}' `pwd` \;

.. note:: ``microbe_root``_dir should be equal ``venv/lib/python2.7/site-packages/Microbe-1.1-py2.7.egg/microbe`` if you installed microbe using virtualenv. If you installed it system wide microbe root dir should be located in ``/usr/local/lib/python2.7/`` 
   
If you installed a Microbe ``pip`` release and whish to upgrade to the latest version you can do it by adding ``--upgrade`` to your command::

    pip install --upgrade microbe

If you installed Microbe using the ``setup.py`` method, simply perform the same steps to install the most recent version.

Then copy back the contents you saved in the first part.
