# Register our models to be viewable in the admin interface.

from django.contrib import admin
from tourny.models import Person

admin.site.register(Person)
