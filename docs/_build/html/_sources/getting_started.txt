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

- Get the last archive `here <https://hg.joacodepel.tk/get_microbe/microbe/archive/tip.zip>`_
- Extract all of it where you whish the site to be stored
- Go to the extracted files
- ``python setup.py install``

Virtualenv note
---------------

Keep in mind that OS will otfen require you to prefix the above commands with ``sudo`` in order to install the app system-wide.

It is recommended to create a virtual environment for Microbe via `virtualenv <http://www.virtualenv.org/>`_ ::

    $ virtualenv $HOME/site
    $ cd $HOME/site
    $ source bin/activate

Then install the app using one of the methods described above.

Upgrading
=========

If you installed a Microbe ``pip`` release and whish to upgrade to the latest version you can do it by adding ``--upgrade`` to your command::

    pip install --upgrade microbe

If you installed Microbe using the ``setup.py`` method, simply perform the same steps to install the most recent version.
