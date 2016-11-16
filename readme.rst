*******
Spotnet
*******

.. contents::
    :local:
    :depth: 1
    :backlinks: none

========
Synopsis
========
TODO

======================================
Setting up the Development Environment
======================================

First Steps
-----------
Start out by cloning this reposity::

    $ git clone https://github.com/welchbj/spotnet

The Backend
-----------
There a few things to install to get the backend up and running. First, make sure to have Python 3.5 installed. Go to the `Python downloads page`_ to get it. It's also recommended that you use `virtualenv`_ to manage Python dependencies. `virtualenvwrapper`_ makes life easier, too. Once you've set these up, make a new virtual environment for spotnet::

    $ mkvirtualenv spotnet

Next, install the backend Python dependencies::

    $ cd backend
    $ pip install -rrequirements.txt

All backend dependencies should now be set up. To run the tests, use::

    $ TODO: command to run the tests

To run an instance of the master server::

    $ TODO: command to run the master server

And to run an instance of the slave server::

    $ TODO: command to run the slave server

The Frontend
------------
Make sure you have a recent version of Node.js installed and on your system's path. Go to the `Node.js downloads page`_ to get it. Next, install `ember-cli`_ and `Gulp`_, using::

    $ npm install -g ember-cli gulp

Next, make sure you are in the frontend directory. You can install all npm and bower dependencies with::

    $ npm install
    $ bower install

You should now be able to build and server the Ember frontend application. Run the live reload server with::

    $ ember serve

Hopefully, all went well and you have the development environment ready to go.

Misc
----
To conform to some of the basic style standards of this project, please make sure you have the proper `editorconfig`_ plugin for your editor or IDE installed.

Note that this project comes with a built JS/CSS dist of our `Semantic UI`_ frontend. This dist will need to be rebuilt if you modify site customization variables in the semantic directoy; to do so, use::

    $ cd semantic
    $ gulp build

====================
Authentication Flows
====================

The Frontend
------------
TODO

The Backend
-----------
TODO

=======
License
=======
Spotnet uses the `MIT License`_.

.. _Python downloads page: https://www.python.org/downloads/
.. _virtualenv: https://virtualenv.readthedocs.org/en/latest/userguide.html
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
.. _Node.js downloads page: https://nodejs.org/en/download/
.. _ember-cli: https://ember-cli.com/
.. _Gulp: http://gulpjs.com/
.. _Semantic UI: http://semantic-ui.com/
.. _editorconfig: http://editorconfig.org/
.. _MIT License: https://opensource.org/licenses/MIT