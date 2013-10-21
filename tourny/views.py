# Views for the tourny app.

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.template import Context

from tourny.forms import PersonForm, PaymentForm
from tourny.models import Payment, Person

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
      person = Person.objects.get(pk=pk)
      person.waiver = True
      person.save()
    # If there are payments, we go to another page to process the payment.
    if len(request.POST.getlist('paid')):
      return accept_payment(request)
  competitors = []
  for competitor in Person.objects.all():
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
    competitors.append(Person.objects.get(pk=pk))
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
  context = {'payments' : Payment.objects.all()}
  return render(request, 'tourny/payments.html', context)
  

@login_required
def payment_detail(request, payment_id):
  payment = get_object_or_404(Payment, pk=payment_id)
  context = {'payment': payment,
             'competitors': payment.person_set.all()}
  return render(request, 'tourny/payment_detail.html', context)


@login_required
def competitor_list(request):
  """Summarized view of competitors."""
  competitors = Person.objects.all()
  context = {'competitors' : competitors}
  return render(request, 'tourny/competitors.html', context)


@login_required
def competitor_detail(request):
  pass


@login_required
def competitor_edit(request):
  pass
