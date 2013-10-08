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

# A person competing in the karate tournament.
class Person(models.Model):
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
