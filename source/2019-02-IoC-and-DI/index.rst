=============================================
Dependency injection and Inversion of Control
=============================================

by Maksym Shalenyi (enkidulan)

Background story
================

Or how Inversion of Control came to be.

.. rst-class:: build

    * imagine that it is the 80s
    * it's golden time of Moore's law
    * complexity of programs is growing exponentially
    * Windows 1.0 is released
    * Balmer peak is invented
    * Inversion of control principle appears

What is IoC is used for?
========================

.. rst-class:: build

    * to increase modularity,
    * to make program extensible,
    * to decouple the execution of a task from implementation,
    * to focus a module on the task it is designed for,
    * to free modules from assumptions about how other systems do what they do and instead rely on contracts,
    * to prevent side effects when replacing a module.

So what is Inversion of Control?
================================

.. rst-class:: build

    * the custom code that expresses the purpose of the program calls into reusable libraries to take care of generic tasks, but with inversion of control, it is the framework that calls into the custom, or task-specific, code.

What Inversion of Control is all about?
=======================================

.. rst-class:: build

      * IoC is all about focusing on business logic


Cases of IoC
============

    * frameworks,
    * callbacks,
    * schedulers,
    * event loops,
    * dependency injection design pattern (creational type),
    * template method design pattern (behavioral type),
    * service locator design pattern (structural type),
    * strategy design pattern (behavioral type).


Dependency injection design pattern
===================================

.. rst-class:: build

    * technique whereby one object (or static method) supplies the dependencies of another object

    * dependency injection involves four roles:

        * the ``service object(s)`` to be used
        * the ``client object`` that is depending on the service(s) it uses
        * the ``interfaces`` that define how the client may use the services
        * the ``injector``, which is responsible for constructing the services and injecting them into the client

Comparing UML diagrams
======================

        DI UML diagram

        .. uml::

            rectangle classA
            rectangle Service1Interface
            rectangle Injector
            rectangle Service1
            classA -> Service1Interface: uses
            Injector .> Service1: **1** creates
            Injector .> classA: **2** injects
            Service1 -> Service1Interface: provides

        vs 'classical' structure UML diagram

        .. uml::

            rectangle classB
            rectangle Service2
            classB .> Service2: **1** creates
            classB -> Service2: **2** uses

Dependency injection use case
=============================

Dependency injection implements IoC through composition.

DI types
========

    * Constructor injection
    * Setter injection
    * Interface injection
    * Other types

Constructor DI
==============

This method requires the client to provide a parameter in a constructor for the dependency.

.. code-block:: python

    class ClassA:

        def __init__(self, service):
            self.service = service;

    # Following code is executed by injector
    service = Service()
    a = ClassA(service)

Setter DI
=========

This method requires the client to provide a setter method for the dependency.

.. code-block:: python

    class ClassB:

        service = None

    # Following code is executed by injector
    service = Service()
    b = ClassB()
    b.service = service

Interface DI
============

This is simply the client publishing a role interface to the setter methods of the client's dependencies. It can be used to establish how the injector should talk to the client when injecting dependencies.

.. code-block:: python

    from zope.interface import Interface, implementer

    class IServiceSetter(Interface):

        def set_service(service):
            pass

    @implementer(IServiceSetter)
    class Client:

        def set_service(self, service):
            self.service = service

Other DI
========

Lot of DI frameworks have other types of injection, for example ``pytest``:

.. code-block:: python

    import pytest

    @pytest.fixture(scope="session")
    def service_fixture():
        yield

    def test_list(service_fixture):
        pass


DI Advantages
=============

    * allows client to be configurable,
    * makes clients more independent and task specific,
    * makes client not care about concrete implementation of the service,
    * reduces boilerplate code,
    * allows concurrent or independent development,
    * decreases coupling between a class and its dependency


DI Disadvantages
================

    * configuration details must be supplied by construction code,
    * can make code difficult to trace,
    * requires more upfront development effort,
    * forces complexity to move out of classes and into the linkages between classes,
    * can encourage dependence on a dependency injection framework.

Examples of DI/IoC in Python
============================

    * python-dependency-injector
    * pytest
    * pinject
    * python-inject
    * ...

python-dependency-injector
==========================

.. code-block:: python

    import dependency_injector.containers as containers
    import dependency_injector.providers as providers

    class Engines(containers.DeclarativeContainer):
        """IoC container of engine providers."""
        gasoline = providers.Factory(example.engines.GasolineEngine)
        diesel = providers.Factory(example.engines.DieselEngine)
        electro = providers.Factory(example.engines.ElectroEngine)

    class Cars(containers.DeclarativeContainer):
        """IoC container of car providers."""
        gasoline = providers.Factory(example.cars.Car, engine=Engines.gasoline)
        diesel = providers.Factory(example.cars.Car,engine=Engines.diesel)
        electro = providers.Factory(example.cars.Car, engine=Engines.electro)

    if __name__ == '__main__':
        gasoline_car = Cars.gasoline()
        diesel_car = Cars.diesel()
        electro_car = Cars.electro()

pytest
======

.. code-block:: python

    import pytest

    @pytest.fixture(scope="session")
    def service_a_fixture():
        yield

    @pytest.fixture(scope="session")
    def service_b_fixture(service_a_fixture):
        yield

    def test_list(service_b_fixture):
        pass

pinject
=======

.. code-block:: python

    >>> class OuterClass(object):
    ...     def __init__(self, inner_class):
    ...         self.inner_class = inner_class
    ...
    >>> class InnerClass(object):
    ...     def __init__(self):
    ...         self.forty_two = 42
    ...
    >>> obj_graph = pinject.new_object_graph()
    >>> outer_class = obj_graph.provide(OuterClass)
    >>> print outer_class.inner_class.forty_two
    42

python-inject
=============

.. code-block:: python

    @inject.autoparams()
    def refresh_cache(cache: RedisCache, db: DbInterface):
        pass

    class User(object):
        cache = inject.attr(Cache)

        def __init__(self, id):
            self.id = id

        def save(self):
            self.cache.save('users', self)

    # `inject.param` is deprecated, use `inject.params` instead.
    @inject.param('cache', Cache)
    def bar(foo, cache=None):
        cache.save('foo', foo)

Questions?
==========

Thank you!
==========

