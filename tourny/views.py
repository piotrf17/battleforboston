# Views for the tourny app.

from django.http import HttpResponseRedirect
from django.shortcuts import render

from tourny.forms import PersonForm

# Registration page for the tournament.  This view is publicy accessible,
# and linked from the root url: battleforboston.com/register
def register(request):
  if request.method == 'POST':
    form = PersonForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/thanks')
  else:
    form = PersonForm()
  return render(request, 'tourny/register.html', {
      'form': form,
      })
