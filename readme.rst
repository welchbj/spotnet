*******
Spotnet
*******

.. image:: ./frontend/public/assets/spotnet-logo.png
    :alt: Spotnet
    :align: center

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

You will also have to set up an application on `Spotify's applications page`_.

The Backend
-----------
There a few things to install to get the backend up and running. First, make sure to have Python 3.5 installed. Go to the `Python downloads page`_ to get it. It's also recommended that you use `virtualenv`_ to manage Python dependencies. `virtualenvwrapper`_ makes life easier, too. Once you've set these up, make a new virtual environment for spotnet::

    $ mkvirtualenv spotnet

Next, install the backend Python dependencies::

    $ cd backend
    $ pip install -rrequirements.txt

To run an instance of the master server::

    $ python -m backend.master --advertise --port=8000 --keyphrase="Brian is the cooliest"

And to run an instance of the slave server::

    $ python -m backend.slave --discover

The Frontend
------------
Make sure you have a recent version of Node.js installed and on your system's path. Go to the `Node.js downloads page`_ to get it. Next, make sure you are in the frontend directory. You can install all npm and bower dependencies with::

    $ npm install
    $ bower install

There are a couple of configuration parameters you must specify in order to integrate with the `Spotify Web API`_ from the frontend. In order to avoid versioning client keys and specific user settings, you must create a file frontend/config/local_config.js. In this file, you must specify the following variables within a JavaScript hash:

- SPOTIFY_CLIENT_ID: This is the client ID that will be indicated in your Spotify application page.

- SPOTIFY_AUTH_REDIRECT_URL: This is the full /auth route, which the Spotify authentication service will redirect to. Note that you need to whitelist this URL within your Spotify application page.

A correctly written local_config.js file for development would look similar to::

    $ cat ./frontend/config/local_config.js
    exports.config = {
      SPOTIFY_CLIENT_ID: 'my client id',
      SPOTIFY_AUTH_REDIRECT_URL: 'http://localhost:4200/auth'
    };

This config file is loaded in Ember's environment.js file (also in the config directory) alongside other environment parameters. You should now be able to build and serve the Ember frontend application. Run the live reload server with::

    $ ember serve

Hopefully, all went well and you have the development environment ready to go. Try navigating to http://localhost:4200, and you should be able to see the Spotnet landing page.

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
In order to access the user's saved songs and playlists, we require access to their information via the `Spotify Web API`_. Note that this is a different API than what is used in the backend to access audio playback, and is used to gather song and playlist metadata.

Since the Spotnet web client provides a Spotify interface independent from the backend Raspberry Pi network, we opted to use Spotify's `Implicit Grant`_ authentication flow. The authentication flow managed by Spotnet is fairly simple, and can be broken down into a few steps.

1. User clicks on "Link your account" button on Spotnet landing page (the index route).

2. User is redirected to the Spotify authentication service.

   * If user accepts to give your application access, the flows continues.

   * If user declines to give your application access, the flow stops.

3. User is redirected to /auth route, where their token is parsed from the redirected URL hash.

   * If /auth route handler can properly parse the returned access token, it loads it into memory and writes it to local storage.

   * If /auth route handler cannot properly parse the returned URL parameters, it redirects to the index route and the authentication flow has ended.

4. User is redirected to /home route, upon which their access token is used to make requests and populate the interface with data.

The access token is written to the browser's local storage in order to survive page refresh. At any time from the /home route, the user has access to the /disconnect route through. Accessing the /disconnect route invalidates the current access token (both in-memory and in local storage) and redirects the user back to the index route.

After retrieval, the access token should be valid for one hour. While Spotnet makes no attempt to refresh this token (nor does there exist the ability to do so in the `Implicit Grant`_ authentication flow), the application will invalidate the current token and redirect the user back to the landing page whenever a network request fails. A message on the landing page prompts the user to attempt re-connecting their account, which will solve the problem of an expired token. This strategy should also work to handle the case where a user manually navigates to the /auth route and specifies their own (invalid) token.

The Backend
-----------
TODO

==============
Special Thanks
==============

TODO

=======
License
=======

Spotnet uses the `MIT License`_.

.. _Spotify's applications page: https://developer.spotify.com/my-applications
.. _Python downloads page: https://www.python.org/downloads/
.. _virtualenv: https://virtualenv.readthedocs.org/en/latest/userguide.html
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
.. _Node.js downloads page: https://nodejs.org/en/download/
.. _Spotify Web API: https://developer.spotify.com/web-api/
.. _ember-cli: https://ember-cli.com/
.. _Gulp: http://gulpjs.com/
.. _Semantic UI: http://semantic-ui.com/
.. _editorconfig: http://editorconfig.org/
.. _Implicit Grant: https://developer.spotify.com/web-api/authorization-guide/#implicit-grant-flow
.. _MIT License: https://opensource.org/licenses/MIT