# Views for the tourny app.

import collections
import csv

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.template import Context

from tourny import models as m
from tourny import bracket, listing, receipt
from tourny.forms import PersonForm, PaymentForm, EventForm

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
      p = m.Payment(amount=form.cleaned_data['amount'])
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
def payment_receipt(request, payment_id):
  payment = get_object_or_404(m.Payment, pk=payment_id)
  people = payment.person_set.all()

  # Generate a pdf response.
  response = HttpResponse(content_type="application/pdf")
  response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

  # TODO(piotrf): don't hardcode payment amount
  receipt.receipt(response, people, 25, payment.amount)

  return response


@login_required
def competitor_list(request):
  """Summarized view of competitors."""
  competitors = m.Person.objects.all()
  context = {'competitors' : competitors}
  return render(request, 'tourny/competitors.html', context)


@login_required
def competitor_csv(request):
  """Most important competitor data in a csv."""
  competitors = m.Person.objects.all()

  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="competitors.csv"'

  writer = csv.writer(response)
  writer.writerow(['Name', 'Email', 'Phone'])
  for competitor in competitors:
    writer.writerow([competitor.name, competitor.email, competitor.phone])

  return response

@login_required
def competitor_detail(request, person_id):
  competitor = get_object_or_404(m.Person, pk=person_id)
  context = {'competitor' : competitor}
  return render(request, 'tourny/competitor_detail.html', context)


@login_required
def competitor_edit(request, person_id):
  competitor = get_object_or_404(m.Person, pk=person_id)
  if request.method == 'POST':
    form = PersonForm(request.POST, instance=competitor)
    if form.is_valid():
      person = form.save()
      return HttpResponseRedirect('../%s' % person_id)
  else:
    form = PersonForm(instance=competitor)
  context = {'form' : form,
             'competitor' : competitor}
  return render(request, 'tourny/competitor_edit.html', context)


@login_required
def event_list(request):
  """Summarized view of events.

  Provides a list of events and gives controls to create, open, edit
  and delete events."""
  context = {'events' : m.Event.objects.all()}
  return render(request, 'tourny/events.html', context)


@login_required
def event_add(request):
  """Add a new event."""
  if request.method == 'POST':
    form = EventForm(request.POST)
    if form.is_valid():
      event = form.save()
      return HttpResponseRedirect('../events')
  else:
    form = EventForm(initial={'state':'C'})
  return render(request, 'tourny/event_add.html', {
      'form' : form
      })


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
  # Team Kumite.
  m.Event.objects.create(name='Default',
                         event_type='V',
                         gender='B',      # Both.
                         age='N',         # College & older.
                         experience='L',  # All.
                         team_size=3)
  # Boston Battle.
  m.Event.objects.create(name='Default',
                         event_type='O',
                         gender='B',      # Both.
                         age='N',         # College & older.
                         experience='L',  # All.
                         team_size=2)
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


@login_required
def event_bracket(request, event_id):
  """Generate a bracket for the event."""
  event = get_object_or_404(m.Event, pk=event_id)

  # Generate a pdf response.
  response = HttpResponse(content_type="application/pdf")
  response['Content-Disposition'] = 'attachment; filename="bracket.pdf"'

  # Gather competitors or teams
  Competitor = collections.namedtuple('Competitor', 'name rank experience school')
  competitors = []
  if event.event_type in ['U', 'A']:
    for competitor in event.competitors.all():
      competitors.append(Competitor(competitor.name,
                                    competitor.formatted_rank(),
                                    competitor.years_training,
                                    competitor.get_school_display()))
  elif event.event_type in ['V', 'O']:
    for team in event.teams.all():
      name = team.name
      if event.event_type == 'O':
        name = team.expanded_name()
      years_training_sum = 0.0
      for competitor in team.members.all():
        years_training_sum += competitor.years_training
      # TODO(piotrf): infer an appropriate school for the team.
      competitors.append(Competitor(name,
                                    '',   # Formatted rank.
                                    years_training_sum,
                                    ''))  # School.

  if event.event_type in ['U', 'V', 'O']:
    ordered_competitors = bracket.seed_bracket(competitors)
    bracket.generate_bracket(response, unicode(event),
                             '2013 - Battle for Boston - NECKC/NAKF',
                             ordered_competitors)
    return response
  elif event.event_type == 'A':
    listing.listing(response, unicode(event), competitors)
    return response
                                    
  return HttpResponseRedirect('../../events')


def get_preregistered_teams_for_event(event):
  """Get the people preregistered for the given event."""
  # Filter by event type and experience level.
  # TODO(piotrf): in the future we may want team events to have experience
  # levels.
  if event.event_type == 'V':
    competitors = m.Person.objects.filter(team_kumite=True)
  elif event.event_type == 'O':
    competitors = m.Person.objects.filter(boston_battle=True)
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
  # Now, arrange all competitors into teams based on team name.
  # This is usually really broken since people can't come up with coherent
  # team names, but at least gives a first approximation.
  teams = {}
  for competitor in filtered_competitors:
    if event.event_type == 'V':
      teamname = competitor.team_kumite_team_name
    elif event.event_type == 'O':
      teamname = competitor.boston_battle_team_name
    else:
      # Shouldn't get here due to check at start of function.
      return []
    teams.setdefault(teamname, []).append(competitor)
  return teams


@login_required
def event_detail_team(request, event_id):
  event = get_object_or_404(m.Event, pk=event_id)
  if event.state == 'C':
    teams = get_preregistered_teams_for_event(event)
    good_teams = {}
    bad_teams = {}
    for teamname, competitors in teams.iteritems():
      if len(competitors) == event.team_size:
        good_teams[teamname] = competitors
      else:
        bad_teams[teamname] = competitors
    context = {'event' : event,
               'team_size' : range(1, event.team_size + 1),
               'teams' : good_teams,
               'bad_teams' : bad_teams}
    return render(request, 'tourny/event_detail_team.html', context)
  elif event.state == 'O':
    prereg_teams = get_preregistered_teams_for_event(event)
    good_teams = {}
    bad_teams = {}
    for teamname, competitors in prereg_teams.iteritems():
      team_exists = False
      for team in event.teams.all():
        if team.name == teamname:
          team_exists = True
      if not team_exists:
        if len(competitors) == event.team_size:
          good_teams[teamname] = competitors
        else:
          bad_teams[teamname] = competitors
    context = {'event' : event,
               'team_size' : range(1, event.team_size + 1),
               'teams' : event.teams.all(),
               'good_teams' : good_teams,
               'bad_teams' : bad_teams}
    return render(request, 'tourny/event_detail_team.html', context)


@login_required
def event_open_team(request, event_id):
  event = get_object_or_404(m.Event, pk=event_id)
  if event.state == 'C':
    event.state = 'O'
    teams = get_preregistered_teams_for_event(event)
    for teamname, competitors in teams.iteritems():
      # We don't check for waivers or paid here, just that the team
      # has the right number of competitors.
      if len(competitors) == event.team_size:
        team = m.Team.objects.create(name=teamname)
        for competitor in competitors:
          team.members.add(competitor)
        team.save()
        event.teams.add(team)
    event.save()
  return HttpResponseRedirect('../%s' % event_id)


@login_required
def event_add_teams(request, event_id):
  """Add teams to a given event."""
  event = get_object_or_404(m.Event, pk=event_id)
  if request.method == 'POST':
    teams = get_preregistered_teams_for_event(event)
    for teamname in request.POST.getlist('add'):
      if teamname in teams:
        team = m.Team.objects.create(name=teamname)
        for competitor in teams[teamname]:
          team.members.add(competitor)
        team.save()
        event.teams.add(team)
    event.save()
  return HttpResponseRedirect('../%s' % event_id)


@login_required
def event_remove_teams(request, event_id):
  """Remove teams from a given event."""
  event = get_object_or_404(m.Event, pk=event_id)
  if request.method == 'POST':
    for pk in request.POST.getlist('remove'):
      event.teams.remove(pk)
      m.Team.objects.get(pk=pk).delete()
  return HttpResponseRedirect('../%s' % event_id)
