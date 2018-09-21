========
Websauna
========

Maksym Shalenyi (enkidulan), 2018


What is websauna?
=================

.. rst-class:: build

    - A full stack Python framework for building consumer and business web applications
    - We have web applications 80% figured out. Websauna takes it up to 95%.
    - Like Django without too much Django in it

Focused on
==========

.. rst-class:: build

    * Maintainability
    * Security
    * Extensibility
    * Lines of code

Features
========

* Theming (Bootstrap)
* Forms
* Session
* Migration
* Admin panel
* Logging/Sing Up
* Caching
* Deployment
* Tasks
* Cookiecutter templates

Storage layer
=============

* PostgreSQL
* SQLAlchemy
* Alembic
* pyramid-tm
* Redis

View layer
==========

* colander
* ColanderAlchemy
* deform
* Jinja2
* Bootstrap

Development
===========

* Addons and application architecture
* cookiecutter
* jupyter-notebook
* pyramid-debugtoolbar

Testing
=======

* pytest
* selenium

Deployment
==========

* ansible


Application structure
=====================

.. code-block:: bash

    ├── alembic
    ├── my
    │   └── app
    │       ├── conf
    │       ├── static
    │       ├── templates
    │       │   ├── email
    │       │   │   └── header.html
    │       │   ├── my.app
    │       │   │   └── home.html
    │       │   └── site
    │       │       ├── css.html
    │       │       └── logo.html
    │       ├── tests
    │       ├── models.py
    │       ├── admins.py
    │       └── views.py
    ├── README.rst
    ├── requirements.txt
    └── setup.py

Views
=====

``request`` object provide a log of useful features out of the box:

* request.registry
* request.dbsession
* request.user
* ...

.. code-block:: python

    @simple_route("/", route_name="home", renderer='my.app/home.html')
    def home(request: Request):
        return (
          request.dbsession
          .query(Page)
          .filter_by(author=request.user)
          .order_by(Page.created_at.desc())
          .first()
        )

Models
======

.. code-block:: python

    class Page(websauna.system.model.meta.Base):
        __tablename__ = "pages"
        id = sa.Column(
            psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"))
        created_at = sa.Column(UTCDateTime, default=now, nullable=False)
        author = sa.orm.relationship("User")
        author_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

        # By default order latest posts first
        __mapper_args__ = {"order_by": created_at.desc()}
        #: Logger efficient representation of model object.
        def __repr__(self) -> str:
            return "#{}: {}".format(self.id, self.title)
        #: Human friendly representation of model object.
        def __str__(self) -> str:
            return self.title

Application initialization
==========================

.. code-block:: python

    class Initializer(websauna.system.Initializer):

        def configure_templates(self):
            """Include our package templates folder in Jinja 2 configuration."""
            super(Initializer, self).configure_templates()
            self.config.add_jinja2_search_path(
                'my.app:templates', name='.html', prepend=True)

        def configure_views(self):
            """Configure views for your application."""
            from . import views
            self.config.scan(views)

        ...

Addon initialization
====================

.. code-block:: python

    class AddonInitializer:

        @after(Initializer.configure_admin)
        def configure_admin(self):
            """Include admin views."""
            from . import admins
            self.config.scan(admins)

        @after(Initializer.configure_templates)
        def configure_templates(self):
            self.config.add_jinja2_search_path(
                "websauna.blog:templates", name=".html", prepend=False)
            from . import templatevars
            self.config.include(templatevars)

        ...

Registry flexibility
====================

`Websauna` framework uses components registry to achieve flexibility.
For example it allows overriding of its built-in models:


.. code-block:: python

    class AddonInitializer:

        def configure_user_models(self):
            super().configure_user_models()
            from websauna.system.user.interfaces import IUserModel
            self.config.registry.registerUtility(myapp.models.User, IUserModel)

    ...

    def my_view(request):
        assert isinstance(request.user, myapp.models.User)

Admin panel
===========

.. code-block:: python

    from websauna.system.admin import modeladmin
    from websauna.system.crud import Base64UUIDMapper

    @modeladmin.model_admin(traverse_id="blog-posts")
    class PostAdmin(modeladmin.ModelAdmin):
        """Manage blog's posts."""

        title = "Blog posts"
        model = Post
        mapper = Base64UUIDMapper(mapping_attribute="id")

        class Resource(modeladmin.ModelAdmin.Resource):
            """Post resource for admin panel."""

            def get_title(self):
                return self.get_object().title

Live demo session
=================

Community
=========

* github - https://github.com/websauna/
* gitter - https://gitter.im/websauna/websauna
* site - https://websauna.org
* twitter - @websauna9000


Thank you
=========

FROM SAUNA WITH LOVE
