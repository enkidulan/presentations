==================
ZCA in modern apps
==================

by Maksym Shalenyi (enkidulan)

.. note::

   * Make sure to mention the important background story for
     this slide.

What ZCA is?
============

.. rst-class:: build

    - ZCA stands for:
        - Zope
        - Component
        - Architecture
    - ZCA is a framework for supporting component based design and programming.
    - ZCA is designed for developing large Python software systems.
    - ZCA is all about spreading the complexity of systems over multiple cooperating components.

ZCA framework
=============

The ZCA is not the components themselves, rather it is about creating,
registering, and retrieving components.

There are three core packages related to the ZCA:

.. rst-class:: build

    * ``zope.interface`` is used to define the interface of a component.
    * ``zope.event`` provides a simple event system.
    * ``zope.component`` deals with creation, registration and retrieval of components.


zope.interface
==============

.. rst-class:: build

    - Interfaces are objects that specify (document) the external behavior of objects that “provide” them. An interface specifies behavior through:

        * Informal documentation in a doc string
        * Attribute definitions
        * Invariants, which are conditions that must hold for objects that provide the interface

    - Components are reusable objects with introspectable interfaces.


Interface
=========

.. literalinclude:: code.py
   :lines: 1, 7-16


Interface
=========

.. literalinclude:: code.py
   :lines: 18-33


Interface
=========

.. literalinclude:: code.py
   :lines: 36-45


Registry
========

Registry provide a way to register objects that depend on one or more interface specifications and provide (perhaps indirectly) some interface. In addition, the registrations have names. (You can think of the names as qualifiers of the provided interfaces.)

.. literalinclude:: code.py
   :lines: 4-5

Utilities
=========

Utilities are self-contained components that provide an interface,
that are looked up by an interface and/or a name.

.. literalinclude:: code.py
   :lines: 48-57

Adapters
========

Adapters are components that are computed from other components to adapt them to some interface.

.. literalinclude:: code.py
   :lines: 60-70

Adapters
========

.. literalinclude:: code.py
   :lines: 72-81

Subscription
============

Provide publish–subscribe messaging pattern realization and a bit more.

Subscription
============

.. literalinclude:: code.py
   :lines: 85-102

Subscription
============

.. literalinclude:: code.py
   :lines: 104-115

Handlers
========

Handlers are typically used to handle events.

.. literalinclude:: code.py
   :lines: 118-132

Real life examples
==================

NOTE: No Plone or Zope products are included into the examples.

Configuration management
========================

Under the hood, Pyramid uses a Zope Component Architecture component registry as its application registry. The Zope Component Architecture is referred to colloquially as the "ZCA."

.. code-block:: python

    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from pyramid.response import Response

    def hello_world(request):
        return Response('Hello World!')

    if __name__ == '__main__':
        with Configurator() as config:
            config.add_route('hello', '/')
            config.add_view(hello_world, route_name='hello')
            app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 6543, app)
        server.serve_forever()


Addons and plugins
==================

Addons, like `pyramid_services`.

.. code-block:: python

    svc = request.find_service(ILoginService)


Guillotina
==========

Guillotina uses interfaces to abstract and define various things including content.

Websauna
========

`Websauna` framework uses ZCA approach for allowing overriding of its built-in models.


.. code-block:: python

    class AddonInitializer:

        def configure_user_models(self):
            super().configure_user_models()
            from websauna.system.user.interfaces import IUserModel
            self.config.registry.registerUtility(myapp.models.User, IUserModel)
    ...

    def my_view(request):
        from websauna.system.user.interfaces import IUserModel
        from zope.interface.verify import verifyObject
        assert isinstance(request.user, myapp.models.User)
        verifyObject(request.user, IUserModel)

Links
=====

* https://zopeinterface.readthedocs.io
* http://muthukadan.net/docs/zca.html
* https://guillotina.readthedocs.io/en/latest/
* https://trypyramid.com/
* https://websauna.org/
* http://www.plone.org/


Questions
=========
