# Register our models to be viewable in the admin interface.

from django.contrib import admin
from tourny.models import Payment,Person

admin.site.register(Payment)
admin.site.register(Person)
