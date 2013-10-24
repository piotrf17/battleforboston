# Bracket generation code, originally written by Brian Neltner.
# TODO(piotrf): this file really needs to be cleaned up / refactored.

import collections
import math
import random
import sys

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.lib.units import inch # create variable with 1 inch in points

##################
# generate a pdf file of a bracket given a seeded list of competitor names
def generate_bracket(response, title, footnote, competitor_names):
  titlefontsize = 24
  footnotefontsize = 10
  bodyfontsize = 10

  competitor_number = len(competitor_names)
  round_number = int(math.ceil(math.log(competitor_number,2)))

# random.shuffle(competitor_names)
  # Fill in "byes".
#    missing_entries = int(math.pow(2,round_number)-competitor_number)
#    if missing_entries > 0:
#        for i in range(0,missing_entries):
#            competitor_names.insert(i * 2 + 1, '   ')

  width, height = landscape(letter)  # Store width and height of page as variables.

  firstround_matches = int(math.pow(2,round_number))

  firstround_height = (height-1.5*inch-footnotefontsize-titlefontsize-bodyfontsize)/(firstround_matches-1)
  firstround_bottommargin = 0.75 * inch + footnotefontsize
  firstround_leftmargin = 0.5 * inch

  # Does the first round fit on the page in landscape?
  fits = (firstround_height > (bodyfontsize + 4))

  if fits : # If it does, then print landscape.
    pdf = Canvas(response, pagesize=landscape(letter)) # Create pdf object.
  else : # If not, try portrait?
    pdf = Canvas(response, pagesize=letter) # Create pdf object.
    # Reset sizes for portrait.
    width, height = letter
    firstround_height = (height-1.5*inch-footnotefontsize-titlefontsize-bodyfontsize)/(firstround_matches-1)
    firstround_bottommargin = 0.75 * inch + footnotefontsize
    firstround_leftmargin = 0.5 * inch
    still_doesnt_fit = (firstround_height < (bodyfontsize + 4))
    if still_doesnt_fit : # If it still doesn't fit, shrink the font size.
      # Floor the spacing between brackets in the first round - 4pt for border and then make that the font size. 
      bodyfontsize = int((height-1.5*inches-footnotefontsize-titlefontsize)/firstround_matches)-4
      # Redo spacings.
      firstround_height = (height-1.5*inch-footnotefontsize-titlefontsize-bodyfontsize)/(firstround_matches-1)
      firstround_bottommargin = 0.75 * inch + footnotefontsize
      firstround_leftmargin = 0.5 * inch

  # Build Header
  pdf.setFont("Helvetica", titlefontsize) # Set the font and size.
  pdf.drawCentredString(.5 * width, height - 0.5 * inch - titlefontsize, title + " - " + str(competitor_number) + " competitors.")

  # Build Footer
  pdf.setFont("Helvetica", footnotefontsize) # Set the font and size.
  pdf.drawCentredString(.5 * width, .5 * inch, footnote)

  # Build Page
  pdf.setFont("Helvetica", bodyfontsize) # Set the font and size.
  round_width = (width - 1 * inch)/(round_number+1)

  round_matches = firstround_matches
  round_height = firstround_height
  round_bottommargin = firstround_bottommargin
  round_leftmargin = firstround_leftmargin

  for i in range(0,round_number+1):
    for j in range(0,round_matches):
      pdf.line(round_leftmargin,round_bottommargin + j * round_height,round_leftmargin + round_width, round_bottommargin + j * round_height)
      if j & 1 == 1:
        pdf.line(round_leftmargin+round_width,round_bottommargin + j *round_height,round_leftmargin+round_width,round_bottommargin + (j-1) * round_height)
      if i == 0: # First Round -- Enter Names
        pdf.drawString(round_leftmargin + 2,round_bottommargin + 2 + j * round_height,competitor_names[j])
#            if i == 1: # Second Round -- Enter Byes
#                if competitor_names[j*2]=='   ':
#                    pdf.drawString(round_leftmargin + 2,round_bottommargin + 2 + j * round_height,competitor_names[j*2+1])
#                if competitor_names[j*2+1]=='   ':
#                    pdf.drawString(round_leftmargin + 2,round_bottommargin + 2 + j * round_height,competitor_names[j*2])                        
    #    if i == round_number: # Print logo under the winner entry
    #        pdf.drawImage("NECKC-logo-highres.png", round_leftmargin + round_width/4, round_bottommargin - round_width/2 - 0.1 * inch,width = round_width/2,height = round_width/2)
    round_matches = round_matches / 2
    round_bottommargin = round_bottommargin + round_height / 2
    round_height = round_height * 2
    round_leftmargin = round_leftmargin + round_width

  pdf.showPage() # Close the page
  pdf.save() # Save the document.


###################
# generate a competition bracket given a seeding    
# competitor_array = [namedtuple(name, experience, school)]
def seed_bracket(competitor_array):
  Competitor = collections.namedtuple('Competitor', 'name experience school')

  ranked_competitor_array=sorted(competitor_array, 
                                 key=lambda competitor_array: competitor_array.experience,
                                 reverse=True)

  competitor_number = len(competitor_array)
  round_number = int(math.ceil(math.log(competitor_number,2)))
  total_number = int(math.pow(2,round_number))
#    if (total_number - competitor_number < 4):
#        total_number = int(math.pow(2,round_number+1))
  if (total_number > 32):
    total_number = 32

  # Fill in "byes".
  missing_entries = int(total_number-competitor_number)
  if missing_entries > 0:
    for i in range(0,missing_entries):
      ranked_competitor_array.append(Competitor(' ',-1,'bye%d'%i))

  # Start optimization.
  seeded_bracket_array=[]
  bracket_score_array=[]
  done=0
  iteration=0
    
  while (done==0):
    # Generate a seeding.
    [seeding_array,seeded_competitor_array]=generate_seeding(ranked_competitor_array,
                                                             competitor_number)
    # Score the seeding.
    bracket_score=bracket_scoring(seeded_competitor_array)

    # If the scoring is zero it is perfect, or timeout at iteration 100
    if (bracket_score==0 or iteration>=100):
      done = 1

    # Append the generated bracket to the array along with the corresponding score.
    seeded_bracket_array.append([bracket_score,seeded_competitor_array])
    iteration = iteration + 1

  # Arrange generated brackets by score.
  sorted_seeded_bracket_array=sorted(seeded_bracket_array, 
                                     key=lambda seeded_bracket_array: seeded_bracket_array[0])

  # Lowest scoring bracket is the actual array to be used.
  seeded_competitor_array = sorted_seeded_bracket_array[0][1]
    
  competitor_names=[]
  for i in range(0,len(seeded_competitor_array)):
    competitor_names.append('%d - '%(seeding_array[i]+1)+seeded_competitor_array[i].name)
  return competitor_names


def bracket_scoring(seeded_competitor_array):
  same_schools=0
  total_number = len(seeded_competitor_array)
  grouping = 2
  multiplier = 3
  for j in range(0,total_number/grouping):
    schools_represented=[]
    for i in range(j*grouping,(j+1)*grouping):
      schools_represented.append(seeded_competitor_array[i].school)
    added_value=0
    for school in schools_represented:
      added_value=schools_represented.count(school)-1+added_value
    same_schools=(added_value/2)*multiplier+same_schools

  grouping = 4
  multiplier = 1
  for j in range(0,total_number/grouping):
    schools_represented=[]
    for i in range(j*grouping,(j+1)*grouping):
      schools_represented.append(seeded_competitor_array[i].school)
    added_value=0
    for school in schools_represented:
      added_value=schools_represented.count(school)-1+added_value
    same_schools=(added_value/2)*multiplier+same_schools

  return same_schools


def generate_seeding(ranked_competitor_array, competitor_number):
  total_number=len(ranked_competitor_array)
  # Places the first three or four competitors.
  seeding_array=[]
  for i in range(0,total_number):
    seeding_array.insert(i,-1)
  seeding_array[0]=0 # Top seed always in slot 0
  seeding_array[total_number/2]=1 # Number two seed in slot num/2

  if total_number > 2: # Seed the next level (3-4th seeds)
    next_set_map=[] # Set up a mapping to randomize the next batch.
    for i in range(2,min([4,competitor_number])): # Fill out actual competitors.
      next_set_map.append(i)
    random.shuffle(next_set_map) # Shuffle actual competitors.
    if competitor_number < 4: # Finish filling out byes if necessary.
      for i in range(max(2,competitor_number),4):
        next_set_map.append(i)
    seeding_array[3*total_number/4]=next_set_map[0]
    seeding_array[1*total_number/4]=next_set_map[1]

  if total_number > 4: # Seed the next level (5-8th seeds)
    next_set_map=[]
    for i in range(4,min([8,competitor_number])): # Fill out actual competitors.
      next_set_map.append(i)
    random.shuffle(next_set_map) # Shuffle actual competitors.
    if competitor_number < 8: # Finishing filling out byes if necessary.
      for i in range(max(4,competitor_number),8):
        next_set_map.append(i)
    seeding_array[3*total_number/8]=next_set_map[0]
    seeding_array[7*total_number/8]=next_set_map[1]
    seeding_array[5*total_number/8]=next_set_map[2]
    seeding_array[1*total_number/8]=next_set_map[3]

  if total_number > 8: # Seed the next level (9-16th seeds)
    next_set_map=[]
    for i in range(8,min([16,competitor_number])): # Fill out actual competitors.
      next_set_map.append(i)
    random.shuffle(next_set_map) # Shuffle actual competitors.
    if competitor_number < 16: # Finishing filling out byes if necessary.
      for i in range(max(8,competitor_number),16):
        next_set_map.append(i)
    seeding_array[3*total_number/16]=next_set_map[0]
    seeding_array[11*total_number/16]=next_set_map[1]
    seeding_array[15*total_number/16]=next_set_map[2]
    seeding_array[7*total_number/16]=next_set_map[3]
    seeding_array[5*total_number/16]=next_set_map[4]
    seeding_array[13*total_number/16]=next_set_map[5]
    seeding_array[9*total_number/16]=next_set_map[6]
    seeding_array[1*total_number/16]=next_set_map[7]

  if total_number > 16: # Seed the next level (17-32nd seeds)
    next_set_map=[]
    for i in range(16,min([32,competitor_number])): # Fill out actual competitors.
      next_set_map.append(i)
    random.shuffle(next_set_map) # Shuffle actual competitors.
    if competitor_number < 32: # Finishing filling out byes if necessary.
      for i in range(max(16,competitor_number),32):
        next_set_map.append(i)
    seeding_array[3*total_number/32]=next_set_map[0]
    seeding_array[19*total_number/32]=next_set_map[1]
    seeding_array[27*total_number/32]=next_set_map[2]
    seeding_array[11*total_number/32]=next_set_map[3]
    seeding_array[15*total_number/32]=next_set_map[4]
    seeding_array[31*total_number/32]=next_set_map[5]
    seeding_array[23*total_number/32]=next_set_map[6]
    seeding_array[7*total_number/32]=next_set_map[7]
    seeding_array[5*total_number/32]=next_set_map[8]
    seeding_array[21*total_number/32]=next_set_map[9]
    seeding_array[29*total_number/32]=next_set_map[10]
    seeding_array[13*total_number/32]=next_set_map[11]
    seeding_array[9*total_number/32]=next_set_map[12]
    seeding_array[25*total_number/32]=next_set_map[13]
    seeding_array[17*total_number/32]=next_set_map[14]
    seeding_array[1*total_number/32]=next_set_map[15]

  seeded_competitor_array=[]
  for i in range(0,len(seeding_array)):
    seeded_competitor_array.append(ranked_competitor_array[seeding_array[i]])
    
  return seeding_array, seeded_competitor_array
