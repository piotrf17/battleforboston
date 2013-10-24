import collections

import reportlab.lib.colors as colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
 
def listing(response, competition, competitor_array, teamkata=False):
  Competitor = collections.namedtuple('Competitor', 'name rank experience school')
  # Our container for 'Flowable' objects
  elements = []
 
  # A large collection of style sheets pre-made for us
  styles = getSampleStyleSheet()
 
  doc = SimpleDocTemplate(response)

  # add the title
  elements.append(Paragraph(competition, styles['Heading1']))

  # build a table of competitors
  if teamkata:
    data = [['Name', ' J1 ', ' J2 ', ' J3 ', 'Ave']]
  else:
    data = [['Name', 'Rank', 'School', ' J1 ', ' J2 ', ' J3 ', 'Ave']]
  for competitor in competitor_array:
    if teamkata:
      data.append([competitor.name,'','','',''])
    else:
      data.append([competitor.name,competitor.rank,competitor.school,'','','',''])
  t = Table(data)
  table_style = []
  for i in range(len(competitor_array)):
    start = 3
    if teamkata:
      start = 1
    table_style.append(('BOX',(start,i+1),(start,i+1),0.25,colors.black))
    table_style.append(('BOX',(start+1,i+1),(start+1,i+1),0.25,colors.black))
    table_style.append(('BOX',(start+2,i+1),(start+2,i+1),0.25,colors.black))
    table_style.append(('BOX',(start+3,i+1),(start+3,i+1),0.25,colors.black))
  table_style.append(('FONTSIZE',(0,0),(-1,0),22))
  table_style.append(('FONTSIZE',(0,1),(-1,-1),14))
  table_style.append(('BOTTOMPADDING',(0,0),(-1,-1),14))
  t.setStyle(TableStyle(table_style))

  elements.append(t)
 
  # Write the document to disk
  doc.build(elements)
