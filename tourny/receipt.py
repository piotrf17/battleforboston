import os

from reportlab import platypus as p
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

from mysite import settings

def drawHeading(canvas, doc):
  width, height = doc.pagesize
  canvas.saveState()

  # Logos.
  nakf_logo_path = os.path.join(settings.BASE_DIR,
                                '../tourny/receipt-NAKF-logo-monochrome.jpg')
  neckc_logo_path = os.path.join(settings.BASE_DIR,
                                 '../tourny/receipt-NECKC-logo-highres.jpg')
  canvas.drawImage(nakf_logo_path, x=1.75*inch, y=height-2.5*inch,
                   width=1.5*inch, height=1.5*inch)
  canvas.drawImage(neckc_logo_path, x=width-3.25*inch, y=height-2.5*inch,
                   width=1.5*inch, height=1.5*inch)

  # Title.
  title = 'Receipt - Battle For Boston 2013 - October 26, 2013'
  canvas.setFont('Times-Bold', 16)
  canvas.drawCentredString(width / 2.0, height - 3 * inch, title)

  canvas.restoreState()

def receipt(response, people, amount_per_person, total):
  doc = p.SimpleDocTemplate(response)
  doc.pagesize = portrait(letter)

  elements = [p.Spacer(1, 2.5*inch)]

  # Create the main table of people.
  data = [['Activity', 'Rate/Unit', 'Count', 'Amount (USD)']]
  for person in people:
    data.append([person.name, '%.2f' % amount_per_person, 1, '%.2f' % amount_per_person])
  data.append(['','','',''])

  # Add in random accounting to make it look official.
  accounting_rows = 3
  data.append(['Sum Fees','','','%.2f' % (len(people) * amount_per_person)])
  if total != len(people) * amount_per_person:
    discount = len(people) * amount_per_person - total
    accounting_rows = 4
    data.append(['Discount','','','-%.2f' % (discount)])
  data.append(['Total','','','%.2f' % (total)])
  data.append(['Paid','','','-%.2f' % (total)])
  data.append(['Final Total','','','0.00'])

  # Draw some lines for style.
  style = p.TableStyle([
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
    ('LINEBELOW', (0, -accounting_rows-2), (-1, -accounting_rows-2), 1, colors.black),
    ('LINEBELOW', (0, -2), (-1, -2), 2, colors.black),
    ('ALIGNMENT', (1, 0), (-1, -1), 'RIGHT'),
    ])
  elements.append(p.Table(data, colWidths=[3*inch, 1*inch, 0.75*inch, 1*inch], style=style))

  elements.append(p.Spacer(1, 1*inch))
  elements.append(p.Paragraph('Thank you for your patronage.',
                              style=ParagraphStyle('centered',alignment=1)))

  doc.build(elements, onFirstPage=drawHeading)

