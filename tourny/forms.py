from django.forms import ModelForm
from django.forms import ValidationError

from tourny.models import Person

# Form for a person, primarily used for the registration page.
class PersonForm(ModelForm):
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

    # If we've signed up for boston battle, we need a team name and partner.
    if boston_battle and not boston_battle_team_name:
      raise ValidationError('Please enter a Boston Battle team name!')
    if boston_battle and not boston_battle_partner_name: 
      raise ValidationError('Please enter your Boston Battle teammate\'s name!')

    return cleaned_data
