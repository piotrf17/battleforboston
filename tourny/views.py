# Views for the tourny app.

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context

from tourny.forms import PersonForm
from tourny.models import Person

def send_registration_email(person):
  email_template = get_template('tourny/registration_email.txt')
  context = Context({'person': person})
  send_mail('Your Battle for Boston registration',
            email_template.render(context),
            'noreply@battleforboston.com',
            [person.email])

# Registration page for the tournament.  This view is publicy accessible,
# and linked from the root url: battleforboston.com/register
def register(request):
  if request.method == 'POST':
    form = PersonForm(request.POST)
    if form.is_valid():
      person = form.save()
      send_registration_email(person)
      return HttpResponseRedirect('/thanks')
  else:
    form = PersonForm()
  return render(request, 'tourny/register.html', {
      'form': form,
      })

# Summarized view of competitors.
@login_required
def competitor_list(request):
  competitors = Person.objects.all()
  context = {'competitors' : competitors}
  return render(request, 'tourny/competitors.html', context)

def competitor_detail(request):
  pass

def competitor_edit(request):
  pass
