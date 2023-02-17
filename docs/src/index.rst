===============
Automate-replit
===============

Introduction
============

This is an async api wrapper for `replit <https://replit.com>`_. It currently features:

- A working replit client
- A User object wrapper
- A Presence update function
- A raw gql interface

Installation
------------

.. code-block:: bash

   pip install git+https://github.com/thatrandomperson5/automate-replit

The library requires Python 3.10 or newer.

Requirements
------------

- Python >= 3.10
- aiohttp >= 3.8.0
- aiolimiter >= 1.0.0


Example
--------
Here is an example ethan-getter

.. code-block:: python
    :caption: Get data about the replit mod not-ethan

    from autoreplit import ReplitClient

    client = ReplitClient()

    async def getEthan():
        ethan = await client.getUserByName("not-ethan")
        print(f"Ethan's id: {ethan.id}")
        print(f"Ethan's follower count: {ethan.followerCount}")
        if ethan.isOnline:
            print("Ethan is online!")
        else:
            print(f"Ethan was last seen {ethan.lastSeen}")
        print(f"Ethan's roles: {ethan.roles}")
        print(f"All of ethan: {ethan}")

    client.run(getEthan())



Contents
=========

.. toctree::

    Home <http://automate-replit.rtfd.io/>
    api



    

