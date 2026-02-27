#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import json
import os

# Register fonts
font_paths = [
    ('Microsoft YaHei', '/usr/share/fonts/truetype/chinese/msyh.ttf'),
    ('SimHei', '/usr/share/fonts/truetype/chinese/SimHei.ttf'),
    ('Times New Roman', '/usr/share/fonts/truetype/english/Times-New-Roman.ttf'),
]

for name, path in font_paths:
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(name, path))
        print(f"Registered font: {name}")

# Load real data
with open('/home/z/my-project/download/abu_dhabi_real_data.json', 'r') as f:
    real_data = json.load(f)

with open('/home/z/my-project/download/abu_dhabi_real_predictions.json', 'r') as f:
    predictions = json.load(f)

# Create document
doc = SimpleDocTemplate(
    '/home/z/my-project/download/Abu_Dhabi_Predictions_27Feb2026_REAL.pdf',
    pagesize=A4,
    rightMargin=1.5*cm,
    leftMargin=1.5*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# Styles
title_style = ParagraphStyle('TitleStyle', fontName='Times New Roman', fontSize=28, leading=36, alignment=TA_CENTER, textColor=colors.HexColor('#1a365d'), spaceAfter=10)
subtitle_style = ParagraphStyle('SubtitleStyle', fontName='Times New Roman', fontSize=14, leading=18, alignment=TA_CENTER, textColor=colors.HexColor('#4a5568'), spaceAfter=5)
race_title_style = ParagraphStyle('RaceTitleStyle', fontName='Times New Roman', fontSize=16, leading=20, alignment=TA_LEFT, textColor=colors.HexColor('#1a365d'), spaceBefore=15, spaceAfter=10)
body_style = ParagraphStyle('BodyStyle', fontName='Times New Roman', fontSize=11, leading=16, alignment=TA_LEFT, textColor=colors.black)
nap_style = ParagraphStyle('NAPStyle', fontName='Times New Roman', fontSize=12, leading=16, alignment=TA_LEFT, textColor=colors.HexColor('#276749'), leftIndent=10)
prediction_style = ParagraphStyle('PredictionStyle', fontName='Times New Roman', fontSize=11, leading=15, alignment=TA_LEFT, textColor=colors.HexColor('#2d3748'), leftIndent=10)

# Build content
story = []

# Cover page
story.append(Spacer(1, 2*cm))
story.append(Paragraph('Elghali AI', title_style))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph('Horse Racing Predictions', subtitle_style))
story.append(Paragraph('REAL DATA from emiratesracing.com', ParagraphStyle('Source', fontName='Times New Roman', fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#276749'))))
story.append(Spacer(1, 0.8*cm))

# Meeting info
meeting_info = [
    ['Date:', '27 February 2026'],
    ['Venue:', 'Abu Dhabi Turf Club, UAE'],
    ['Surface:', 'Turf | Going: Good'],
    ['Total Races:', '7'],
]
meeting_table = Table(meeting_info, colWidths=[3*cm, 8*cm])
meeting_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a5568')),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(meeting_table)

story.append(Spacer(1, 0.8*cm))

# Summary table
summary_header = [['Race', 'Name', 'Runners', 'NAP', 'Next Best']]
summary_data = []
for pred in predictions['predictions']:
    summary_data.append([
        f"R{pred['race']}",
        pred['name'][:22],
        str(pred['horses_count']),
        pred['prediction']['nap']['horse'],
        pred['prediction']['next_best']['horse']
    ])

summary_table = Table([summary_header[0]] + summary_data, colWidths=[1.2*cm, 4.2*cm, 1.5*cm, 4*cm, 4*cm])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
]))
story.append(summary_table)

story.append(PageBreak())

# Detailed predictions
for pred in predictions['predictions']:
    # Race header
    race_header = f"Race {pred['race']}: {pred['name']} ({pred['horses_count']} runners)"
    story.append(Paragraph(race_header, race_title_style))
    
    # NAP
    story.append(Paragraph(f"<b>NAP (Best Bet):</b> {pred['prediction']['nap']['horse']}", nap_style))
    story.append(Paragraph(f"<i>{pred['prediction']['nap']['reason']}</i>", prediction_style))
    story.append(Spacer(1, 0.2*cm))
    
    # Next Best
    story.append(Paragraph(f"<b>Next Best:</b> {pred['prediction']['next_best']['horse']}", body_style))
    story.append(Paragraph(f"<i>{pred['prediction']['next_best']['reason']}</i>", prediction_style))
    story.append(Spacer(1, 0.2*cm))
    
    # Each Way
    story.append(Paragraph(f"<b>Each Way Value:</b> {pred['prediction']['each_way']['horse']}", body_style))
    story.append(Paragraph(f"<i>{pred['prediction']['each_way']['reason']}</i>", prediction_style))
    story.append(Spacer(1, 0.2*cm))
    
    # Top 3
    story.append(Paragraph(f"<b>Top 3:</b> {' > '.join(pred['prediction']['top_3'])}", body_style))
    story.append(Spacer(1, 0.2*cm))
    
    # Analysis
    story.append(Paragraph(f"<b>Analysis:</b> {pred['prediction']['analysis']}", prediction_style))
    
    # Show actual horses
    race_data = real_data['races'][pred['race']-1]
    active_horses = [h for h in race_data['horses'] if not h.get('isNR') and h.get('jockey') and h['jockey'] != '-']
    
    if active_horses:
        story.append(Spacer(1, 0.3*cm))
        horse_header = [['#', 'Draw', 'Horse', 'Jockey', 'Rating']]
        horse_data = [[str(h.get('number', '')), str(h.get('draw', '')), h['name'][:16], h['jockey'][:16] if h.get('jockey') else '', str(h.get('rating', 0))] for h in active_horses[:6]]
        
        if horse_data:
            horse_table = Table([horse_header[0]] + horse_data, colWidths=[0.8*cm, 1*cm, 3.5*cm, 3.5*cm, 1.2*cm])
            horse_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#e2e8f0')),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            story.append(horse_table)
    
    story.append(Spacer(1, 0.5*cm))

# Disclaimer
story.append(Spacer(1, 0.3*cm))
disclaimer = """<b>Data Source:</b> Emirates Racing Authority (emiratesracing.com) - Real race card data.

<b>Disclaimer:</b> AI-generated predictions. Gamble responsibly."""
story.append(Paragraph(disclaimer, ParagraphStyle('Disclaimer', fontName='Times New Roman', fontSize=9, leading=12, textColor=colors.HexColor('#718096'), alignment=TA_CENTER)))

# Build PDF
doc.build(story)

print("\n✓ PDF generated successfully!")
print("File: /home/z/my-project/download/Abu_Dhabi_Predictions_27Feb2026_REAL.pdf")
