# Register our models to be viewable in the admin interface.

from django.contrib import admin
from tourny.models import *

admin.site.register(Payment)
admin.site.register(Person)
admin.site.register(Team)
admin.site.register(Event)
