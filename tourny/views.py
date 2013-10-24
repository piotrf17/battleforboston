# Views for the tourny app.

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.template import Context

from tourny import models as m
from tourny.forms import PersonForm, PaymentForm

###################################################################
# Registration Components.
#
# These views and functions are publicly accessible since they are
# part of the registration flow.  Due to a probably poor design,
# these views are actually called from the main site url conf.
###################################################################

def send_registration_email(person):
  email_template = get_template('tourny/registration_email.txt')
  context = Context({'person': person})
  send_mail('Your Battle for Boston registration',
            email_template.render(context),
            'noreply@battleforboston.com',
            [person.email])


def register(request):
  """View for tournament registration page.

  This view is publicy accessible, and linked from the 
  root url: battleforboston.com/register
  """
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

###################################################################
# Tournament control.
#
# These views and functions control the tournament.  All views
# should have a @login_required decorator.
###################################################################

@login_required
def checkin(request):
  """View for competitor check-in.
  
  Select the people you want to take in waivers and payments for, and they
  are processed as a single group.
  """
  if request.method == 'POST':
    # Process waivers silently.
    for pk in request.POST.getlist('waiver'):
      person = m.Person.objects.get(pk=pk)
      person.waiver = True
      person.save()
    # If there are payments, we go to another page to process the payment.
    if len(request.POST.getlist('paid')):
      return accept_payment(request)
  competitors = []
  for competitor in m.Person.objects.all():
    if competitor.paid == False or competitor.waiver == False:
      competitors.append(competitor)
  context = {'competitors' : competitors}
  return render(request, 'tourny/checkin.html', context)


@login_required
def accept_payment(request):
  # We should only reach this method from a post via checkin.
  if request.method != 'POST':
    return HttpResponseRedirect('checkin')

  # Collect all competitors objects for people that we're paying for.
  competitors = []
  cost_per_competitor = 25   # TODO(piotrf): don't hardcode the cost.
  for pk in request.POST.getlist('paid'):
    competitors.append(m.Person.objects.get(pk=pk))
  estimated_cost = cost_per_competitor * len(competitors)

  if 'amount' in request.POST:
    form = PaymentForm(request.POST)
    if form.is_valid():
      p = Payment(amount=form.cleaned_data['amount'])
      p.save()
      for competitor in competitors:
        p.person_set.add(competitor)
        competitor.paid = True
        competitor.save()
      p.save()
      return HttpResponseRedirect('payments/%d' % p.pk)
  else:
    form = PaymentForm({'amount': estimated_cost})

  context = {'competitors' : competitors,
             'estimated_cost' : estimated_cost,
             'form' : form}
  return render(request, 'tourny/accept_payment.html', context)


@login_required
def payment_list(request):
  context = {'payments' : m.Payment.objects.all()}
  return render(request, 'tourny/payments.html', context)
  

@login_required
def payment_detail(request, payment_id):
  payment = get_object_or_404(m.Payment, pk=payment_id)
  context = {'payment': payment,
             'competitors': payment.person_set.all()}
  return render(request, 'tourny/payment_detail.html', context)


@login_required
def competitor_list(request):
  """Summarized view of competitors."""
  competitors = m.Person.objects.all()
  context = {'competitors' : competitors}
  return render(request, 'tourny/competitors.html', context)


@login_required
def competitor_detail(request):
  pass


@login_required
def competitor_edit(request):
  pass


@login_required
def event_list(request):
  """Summarized view of events.

  Provides a list of events and gives controls to create, open, edit
  and delete events."""
  context = {'events' : m.Event.objects.all()}
  return render(request, 'tourny/events.html', context)


@login_required
def event_delete(request):
  """Delete a set of events."""
  if request.method == 'POST':
    for pk in request.POST.getlist('delete'):
      m.Event.objects.get(pk=pk).delete()
  return HttpResponseRedirect('../events')


@login_required
def generate_default_events(request):
  """Create the default events for the tournament.

  Create a predefined set of events, and prepopulate based on event
  characteristics."""
  # Individual Kumite events.
  for gender in ['M', 'F']:
    for age in ['Y', 'C', 'O']:
      for experience in ['B', 'I', 'A']:
        m.Event.objects.create(name='Default',
                               event_type='U',
                               gender=gender,
                               age=age,
                               experience=experience)
  # Individual Kata events.
  for age in ['Y', 'N']:
    for experience in ['B', 'I', 'A']:
      m.Event.objects.create(name='Default',
                             event_type='A',
                             gender='B',
                             age=age,
                             experience=experience)
  return HttpResponseRedirect('../events')


def get_preregistered_for_event(event):
  """Get the people preregistered for the given event."""
  # Filter by event type and experience level.
  # TODO(piotrf): handle event experience level of "All"
  if event.event_type == 'A':
    competitors = m.Person.objects.filter(kata=event.experience)
  elif event.event_type == 'U':
    competitors = m.Person.objects.filter(kumite=event.experience)
  else:
    return []
  # Filter by gender.
  if event.gender != 'B':
    competitors = competitors.filter(gender=event.gender)
  # Filter by age.
  filtered_competitors = []
  for competitor in competitors:
    if (event.age == 'A' or 
        event.age == competitor.age_division() or
        (event.age == 'N' and (competitor.age_division() == 'C' or
                               competitor.age_division() == 'O'))):
      filtered_competitors.append(competitor)
  return filtered_competitors


@login_required
def event_detail(request, event_id):
  event = get_object_or_404(m.Event, pk=event_id)
  if event.state == 'C':
    competitors_prereg_check = []
    competitors_prereg = []
    for competitor in get_preregistered_for_event(event):
      if competitor.paid and competitor.waiver:
        competitors_prereg_check.append(competitor)
      else:
        competitors_prereg.append(competitor)
    context = {'event' : event,
               'competitors_prereg_check' : competitors_prereg_check,
               'competitors_prereg' : competitors_prereg}
    return render(request, 'tourny/event_detail.html', context)
  elif event.state == 'O':
    # We have 3 different sets of competitors:
    #   event_competitors = people currently in the event
    #   event_competitors_prereg = registered, but not in the event
    #   other_competitors = everyone else
    # The reason is that when the event is opened, some competitors may not have
    # finished registration yet, and so will not be put in the event unless
    # manually overridden.
    event_competitors = event.competitors.all()
    event_competitors_prereg = []
    for competitor in get_preregistered_for_event(event):
      if competitor not in event_competitors:
        event_competitors_prereg.append(competitor)
    other_competitors = []
    for competitor in m.Person.objects.all():
      if (competitor not in event_competitors and
          competitor not in event_competitors_prereg):
        other_competitors.append(competitor)
    context = {'event' : event,
               'event_competitors' : event_competitors,
               'event_competitors_prereg' : event_competitors_prereg,
               'other_competitors' : other_competitors}
    return render(request, 'tourny/event_detail.html', context)


@login_required
def event_open(request, event_id):
  event = get_object_or_404(m.Event, pk=event_id)
  if event.state == 'C':
    event.state = 'O'
    for competitor in get_preregistered_for_event(event):
      if competitor.paid and competitor.waiver:
        event.competitors.add(competitor)
    event.save()
  return HttpResponseRedirect('../%s' % event_id)

@login_required
def event_add_competitors(request, event_id):
  """Add competitors to a given event."""
  event = get_object_or_404(m.Event, pk=event_id)
  if request.method == 'POST':
    for pk in request.POST.getlist('add'):
      event.competitors.add(pk)
  return HttpResponseRedirect('../%s' % event_id)


@login_required
def event_remove_competitors(request, event_id):
  """Remove competitors from a given event."""
  event = get_object_or_404(m.Event, pk=event_id)
  if request.method == 'POST':
    for pk in request.POST.getlist('remove'):
      event.competitors.remove(pk)
  return HttpResponseRedirect('../%s' % event_id)
