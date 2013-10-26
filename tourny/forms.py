from django.forms import Form, IntegerField, ModelForm, ValidationError

from tourny.models import Person, Event

class PersonForm(ModelForm):
  """Form for a person, primarily used for the registration page."""

  class Meta:
    model = Person

  def clean(self):
    cleaned_data = super(PersonForm, self).clean()
    kata = cleaned_data.get('kata')
    kumite = cleaned_data.get('kumite')
    team_kumite = cleaned_data.get('team_kumite')
    team_kumite_team_name = cleaned_data.get('team_kumite_team_name')
    boston_battle = cleaned_data.get('boston_battle')
    boston_battle_team_name = cleaned_data.get('boston_battle_team_name')
    boston_battle_partner_name = cleaned_data.get('boston_battle_partner_name')

    # Check that we've signed up for at least one event.
    if not kata and not kumite and not team_kumite and not boston_battle:
      raise ValidationError('You must sign up for at least one event!')

    # If we've signed up for team kumite, make sure we have a team name.
    if team_kumite and not team_kumite_team_name:
      raise ValidationError('Please enter a team kumite team name!')
    if team_kumite_team_name and not team_kumite:
      raise ValidationError('You entered a team kumite team name, ' +
                            'but did not select that you want to participate ' +
                            'in team kumite.  Please check the box below.')

    # If we've signed up for boston battle, we need a team name and partner.
    if boston_battle and not boston_battle_team_name:
      raise ValidationError('Please enter a Boston Battle team name!')
    if boston_battle_team_name and not boston_battle:
      raise ValidationError('You entered a Boston Battle team name, ' +
                            'but did not select that you want to participate ' +
                            'in Boston Battle.  Please check the box below.')
    if boston_battle and not boston_battle_partner_name: 
      raise ValidationError('Please enter your Boston Battle teammate\'s name!')

    return cleaned_data


class PaymentForm(Form):
  """Form for taking in a payment

  The payment amount is an editable field, the list of people
  being paid for is a hidden field."""
  
  amount = IntegerField(min_value=0)


class EventForm(ModelForm):
  """Form for a new event."""
  
  class Meta:
    model = Event
    fields = ('name', 'event_type', 'gender', 'age', 'experience', 'team_size')

  def clean(self):
    cleaned_data = super(EventForm, self).clean()

    # Boston battle has 2 person teams.
    event_type = cleaned_data.get('event_type')
    team_size = cleaned_data.get('team_size')
    if event_type == 'O' and team_size != 2:
      raise ValidationError('Boston battle has 2 person teams!')

    return cleaned_data
