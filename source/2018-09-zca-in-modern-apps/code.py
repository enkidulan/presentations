import zope.interface
import zope.interface.verify
from zope.interface.adapter import AdapterRegistry
from zope.interface.registry import Components
registry = Components()


class IFoo(zope.interface.Interface):
    """Foo blah blah"""
    x = zope.interface.Attribute("""X blah blah""")

class IBaz(IFoo):
    """Baz blah"""

    def eek(a=1):
        """eek in baz blah"""

@zope.interface.implementer(IBaz)
class Bazz:

    def __init__(self, x=None):
        self.x = x

    def eek(self, a=1):
        return a

assert IFoo.implementedBy(Bazz)
assert IBaz.implementedBy(Bazz)

bazz = Bazz()
assert IFoo.providedBy(bazz)
assert IBaz.providedBy(bazz)
assert zope.interface.verify.verifyObject(IBaz, bazz)


class Bar(Bazz):
    pass

assert IFoo.implementedBy(Bar)
assert IBaz.implementedBy(Bar)

bar = Bar()
assert IFoo.providedBy(bar)
assert IBaz.providedBy(bar)
assert zope.interface.verify.verifyObject(IBaz, bar)


bob = Bazz('bob')
ted = Bazz('ted')

registry.registerUtility(bob)
assert registry.queryUtility(IBaz) == bob

registry.registerUtility(ted, IBaz, name='ted')
assert registry.queryUtility(IFoo, 'ted') == ted

assert registry.getAllUtilitiesRegisteredFor(IBaz) == [bob, ted]

# adapter
class IGreeter(zope.interface.Interface):
    def greet():
        """Greet someone."""

class IPerson(zope.interface.Interface):
    name = zope.interface.Attribute("Name")

@zope.interface.implementer(IPerson)
class Person:
    def __init__(self, name):
        self.name = name

@zope.interface.implementer(IGreeter)
class PersonGreeter(object):
    def __init__(self, person: IPerson):
        self.person = person

    def greet(self):
        return "Hello " + self.person.name

registry.registerAdapter(PersonGreeter, [IPerson], IGreeter)
assert registry.queryAdapter(Person("Sally"), IGreeter).greet() == "Hello Sally"


####
class IFire(zope.interface.Interface):
    pass

@zope.interface.implementer(IFire)
class Fire(object):
    pass

class IFireExtinguisher(zope.interface.Interface):
    def extinguish():
        pass

@zope.interface.implementer(IFireExtinguisher)
class FireExtinguisher(object):
    def __init__(self, context: IFire):
        self.context = context

    def extinguish(self):
        return self.__class__.__name__

class PowderExtinguisher(FireExtinguisher):
    pass

class SprinklerSystem(FireExtinguisher):
    pass

registry.registerSubscriptionAdapter(PowderExtinguisher, (IFire,))
registry.registerSubscriptionAdapter(SprinklerSystem, (IFire,), IFireExtinguisher)

extinguishers = registry.subscribers((Fire(),), IFireExtinguisher)
extinguishers_results = [extinguisher.extinguish() for extinguisher in extinguishers]
assert (extinguishers_results == ['PowderExtinguisher', 'SprinklerSystem'])


class IDocumentCreated(zope.interface.Interface):
    doc = zope.interface.Attribute("The document that was created")

@zope.interface.implementer(IDocumentCreated)
class DocumentCreated(object):
    def __init__(self, doc):
        self.doc = doc

def setCreationDate(event: IDocumentCreated):
    event.doc['created'] = 'now'

doc = {}
registry.registerHandler(setCreationDate, (IDocumentCreated,))  # handler registration
registry.handle(DocumentCreated(doc))  # initiation of event handlers
assert doc == {'created': 'now'}
