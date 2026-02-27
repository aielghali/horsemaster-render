#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.units import cm, mm
import json
import os

# Register fonts
pdfmetrics.registerFont(TTFont('Microsoft YaHei', '/usr/share/fonts/truetype/chinese/msyh.ttf'))
pdfmetrics.registerFont(TTFont('SimHei', '/usr/share/fonts/truetype/chinese/SimHei.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman', '/usr/share/fonts/truetype/english/Times-New-Roman.ttf'))
registerFontFamily('Microsoft YaHei', normal='Microsoft YaHei', bold='Microsoft YaHei')
registerFontFamily('Times New Roman', normal='Times New Roman', bold='Times New Roman')

# Load predictions
with open('/home/z/my-project/download/abu_dhabi_predictions.json', 'r') as f:
    data = json.load(f)

# Create document
doc = SimpleDocTemplate(
    '/home/z/my-project/download/Abu_Dhabi_Race_Predictions_27Feb2026.pdf',
    pagesize=A4,
    rightMargin=1.5*cm,
    leftMargin=1.5*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# Styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'TitleStyle',
    fontName='Microsoft YaHei',
    fontSize=28,
    leading=36,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#1a365d'),
    spaceAfter=10
)

subtitle_style = ParagraphStyle(
    'SubtitleStyle',
    fontName='Times New Roman',
    fontSize=14,
    leading=18,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#4a5568'),
    spaceAfter=5
)

race_title_style = ParagraphStyle(
    'RaceTitleStyle',
    fontName='Times New Roman',
    fontSize=16,
    leading=20,
    alignment=TA_LEFT,
    textColor=colors.HexColor('#1a365d'),
    spaceBefore=15,
    spaceAfter=10
)

body_style = ParagraphStyle(
    'BodyStyle',
    fontName='Times New Roman',
    fontSize=11,
    leading=16,
    alignment=TA_LEFT,
    textColor=colors.black
)

prediction_style = ParagraphStyle(
    'PredictionStyle',
    fontName='Times New Roman',
    fontSize=11,
    leading=15,
    alignment=TA_LEFT,
    textColor=colors.HexColor('#2d3748'),
    leftIndent=10
)

nap_style = ParagraphStyle(
    'NAPStyle',
    fontName='Times New Roman',
    fontSize=12,
    leading=16,
    alignment=TA_LEFT,
    textColor=colors.HexColor('#276749'),
    leftIndent=10
)

# Build content
story = []

# Cover page
story.append(Spacer(1, 3*cm))
story.append(Paragraph('Elghali AI', title_style))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph('حصيفلا تاراشتلا', ParagraphStyle('ArabicTitle', fontName='Microsoft YaHei', fontSize=24, alignment=TA_CENTER, textColor=colors.HexColor('#1a365d'))))
story.append(Spacer(1, 1*cm))
story.append(Paragraph('Horse Racing Predictions', subtitle_style))
story.append(Spacer(1, 0.5*cm))

# Meeting info
meeting_info = [
    ['Date:', '27 February 2026'],
    ['Venue:', 'Abu Dhabi Turf Club, UAE'],
    ['Surface:', 'Turf'],
    ['Going:', 'Good'],
    ['Races:', '7']
]

meeting_table = Table(meeting_info, colWidths=[3*cm, 8*cm])
meeting_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a5568')),
    ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(meeting_table)

story.append(Spacer(1, 1*cm))

# Summary box
summary_data = [['Summary of Predictions']]
summary_table = Table(summary_data, colWidths=[16*cm])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a365d')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 14),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
]))
story.append(summary_table)

# NAP Summary
nap_summary = [['Race', 'NAP (Best Bet)', 'Next Best', 'Each Way Value']]
for pred in data['predictions']:
    nap_summary.append([
        f"R{pred['race']}",
        pred['prediction']['nap']['horse'],
        pred['prediction']['next_best']['horse'],
        pred['prediction']['each_way']['horse']
    ])

nap_table = Table(nap_summary, colWidths=[2*cm, 4.5*cm, 4.5*cm, 4.5*cm])
nap_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
]))
story.append(nap_table)

story.append(PageBreak())

# Detailed predictions for each race
for pred in data['predictions']:
    # Race header
    race_header = f"Race {pred['race']}: {pred['name']} ({pred['distance']}) - {pred['time']}"
    story.append(Paragraph(race_header, race_title_style))
    
    # NAP
    nap_text = f"<b>NAP (Best Bet):</b> {pred['prediction']['nap']['horse']}"
    story.append(Paragraph(nap_text, nap_style))
    story.append(Paragraph(f"<i>Reason: {pred['prediction']['nap']['reason']}</i>", prediction_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Next Best
    next_text = f"<b>Next Best:</b> {pred['prediction']['next_best']['horse']}"
    story.append(Paragraph(next_text, body_style))
    story.append(Paragraph(f"<i>Reason: {pred['prediction']['next_best']['reason']}</i>", prediction_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Each Way
    eachway_text = f"<b>Each Way Value:</b> {pred['prediction']['each_way']['horse']}"
    story.append(Paragraph(eachway_text, body_style))
    story.append(Paragraph(f"<i>Reason: {pred['prediction']['each_way']['reason']}</i>", prediction_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Top 3
    top3_text = f"<b>Top 3 Prediction:</b> {' → '.join(pred['prediction']['top_3'])}"
    story.append(Paragraph(top3_text, body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Analysis
    analysis_text = f"<b>Race Analysis:</b> {pred['prediction']['analysis']}"
    story.append(Paragraph(analysis_text, prediction_style))
    
    story.append(Spacer(1, 0.5*cm))

# Disclaimer
story.append(Spacer(1, 1*cm))
disclaimer = """<b>Important Notice:</b> These predictions are generated by Elghali AI based on available data analysis. 
Horse racing involves inherent risks, and past performance does not guarantee future results. 
Please gamble responsibly and only bet what you can afford to lose. 
These predictions are for informational purposes only and should not be considered as financial or betting advice."""
story.append(Paragraph(disclaimer, ParagraphStyle('Disclaimer', fontName='Times New Roman', fontSize=9, leading=12, textColor=colors.HexColor('#718096'), alignment=TA_CENTER)))

# Build PDF
doc.build(story)

print("PDF generated successfully!")
print("File: /home/z/my-project/download/Abu_Dhabi_Race_Predictions_27Feb2026.pdf")
