import datetime

from django.db import models
from localflavor.us.models import PhoneNumberField
from localflavor.us.models import USStateField
from south.modelsinspector import add_introspection_rules

# South introspection rules for localflavor fields.
add_introspection_rules([], ["^localflavor\.us\.models\.PhoneNumberField"])
add_introspection_rules([], ["^localflavor\.us\.models\.USStateField"])

KARATE_SCHOOLS = (
  ('non', 'Non-NECKC/NAKF school'),
  ('BC', 'BC Shotokan Karate'),
  ('BU', 'BU Shotokan Karate'),
  ('MIT', 'MIT Shotokan Karate'),
  ('MITSKD', 'MIT STKD'),
  ('UMass', 'Umass Lowell Shotokan'),
  ('Tufts', 'Tufts Shotokan Karate'),
  ('BW', 'Bridgewater Shotokan Karate'),
  ('HH', 'Haverhill (NAKF)'),
  ('Lynn', 'Lynn (NAKF)'),
  ('Bermuda', 'Bermuda (NAKF)'),
  ('Wyoming', 'Wyoming Valley (NAKF)'),
  ('Concord', 'Concord (NAKF)'),
  ('Tiger', 'Tiger Mountain (NAKF)'),
  ('Claremont', 'Claremont NH (NAKF)'),
  ('Rossini', 'Rossini Karate'),
)


class Payment(models.Model):
  """A payment to the tournament for a set of competitors."""
  
  amount = models.IntegerField()

  def __unicode__(self):
    return 'Amount: $%d' % self.amount


class Person(models.Model):
  """A person competing in the karate tournament."""

  GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
  )

  KYU_OR_DAN = (
    ('K', 'Kyu'),
    ('D', 'Dan'),
  )

  EVENT_CHOICES = (
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),
  )

  # Basic information.
  name = models.CharField(max_length=100)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  dob = models.DateField('date of birth')
  college_age = models.BooleanField(blank=True)
  
  # Contact information.
  email = models.EmailField(max_length=254)
  phone = PhoneNumberField()
  address1 = models.CharField(max_length=100)
  address2 = models.CharField(max_length=100, blank=True)
  city = models.CharField(max_length=50)
  state = USStateField(default='MA')
  zipcode = models.CharField(max_length=10)

  # Emergency contact.
  emergency_contact_name = models.CharField(max_length=100)
  emergency_contact_relation = models.CharField(max_length=50)
  emergency_contact_phone = PhoneNumberField()

  # Karate Experience.
  rank = models.CharField(max_length=10, blank=True)
  kyu_or_dan = models.CharField(max_length=1, choices=KYU_OR_DAN, default='K')
  belt_color = models.CharField(max_length=20, blank=True)
  years_training = models.FloatField()
  school = models.CharField(max_length=10, choices=KARATE_SCHOOLS)

  # Events.
  kata = models.CharField(max_length=1, choices=EVENT_CHOICES, blank=True)
  kumite = models.CharField(max_length=1, choices=EVENT_CHOICES, blank=True)
  team_kumite = models.BooleanField(blank=True)
  team_kumite_team_name = models.CharField(max_length=100, blank=True)
  boston_battle = models.BooleanField(blank=True)
  boston_battle_team_name = models.CharField(max_length=100, blank=True)
  boston_battle_partner_name = models.CharField(max_length=100, blank=True)

  # Check-in state.
  waiver = models.BooleanField(blank=True, default=False)
  paid = models.BooleanField(blank=True, default=False)

  payment = models.ForeignKey(Payment, blank=True, null=True, on_delete=models.SET_NULL)

  def __unicode__(self):
    return self.name

  def age(self):
    today = datetime.date.today()
    if (today.month > self.dob.month or
        (today.month == self.dob.month and today.day >= self.dob.day)):
      return today.year - self.dob.year
    else:
      return today.year - self.dob.year + 1

  def age_division(self):
    if self.college_age:
      return 'C'
    if self.age() > 25:
      return 'O'
    elif self.age() > 18:
      return 'C'
    else:
      return 'Y'

class Team(models.Model):
  """A team of people that compete in an event."""
  
  name = models.CharField(max_length=100)
  members = models.ManyToManyField(Person)

  def __unicode__(self):
    return self.name


class Event(models.Model):
  """An event that competitors/teams can participate in."""

  GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('B', 'Both'),
  )

  EVENT_TYPE_CHOICES = (
    ('A', 'Kata'),
    ('B', 'Team Kata'),
    ('U', 'Kumite'),
    ('V', 'Team Kumite'),
    ('B', 'Boston Battle'),
  )

  AGE_CHOICES = (
    ('Y', 'Youth'),
    ('C', 'College'),
    ('O', 'Older'),
    ('N', 'College and Older'),
    ('A', 'All'),
  )

  EXPERIENCE_CHOICES = (
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),
    ('L', 'All'),
  )

  EVENT_STATES_CHOICES = (
    ('C', 'Created'),
    ('O', 'Open'),
    ('F', 'Finished'),
  )

  # Basic event information.
  name = models.CharField(max_length=100)
  event_type = models.CharField(max_length=1, choices=EVENT_TYPE_CHOICES)

  # Division slicing parameters for events.  Mostly useful for prepopulating
  # the event with people that fit the slice.
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  age = models.CharField(max_length=1, choices=AGE_CHOICES)
  experience = models.CharField(max_length=1, choices=EXPERIENCE_CHOICES)

  competitors = models.ManyToManyField(Person)

  team_size = models.IntegerField(default=3)
  teams = models.ManyToManyField(Team)

  state = models.CharField(max_length=1, choices=EVENT_STATES_CHOICES,
                           default='C')

  def __unicode__(self):
    return self.name
