The topic of presentation is Dependency injection and Inversion of Control.

Please talk about what problem DI solves, the types of DIs, relation of DI to Design Patters, examples of DI/IoC in your favorite language.

=============================================
Dependency injection and Inversion of Control
=============================================

by Maksym Shalenyi (enkidulan)

Background story
================

Or how Inversion of Control become to be.

.. rst-class:: build

    * imagen that it is 198x
    * it's golden time Moore's law
    * complexity of programs is growing exponentially
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

.. rst-class:: build

    * frameworks,
    * callbacks,
    * schedulers,
    * event loops,
    * dependency injection design pattern,
    * template method design pattern,
    * service locator design pattern,
    * strategy design pattern.


Dependency injection design pattern
===================================

.. rst-class:: build

    * technique whereby one object (or static method) supplies the dependencies of another object

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
Lot of DI frameworks have other types of injection beyond those presented above, for example ``pytest``:

.. code-block:: python

    import pytest

    @pytest.fixture(scope="session")
    def service_fixture():
        yield

    def test_list(service_fixture):
        pass
