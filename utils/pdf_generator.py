def generate_job_card_pdf(
	jobcard_number, name, phone, place, bike_no, model, year, engine_no, chasis_no,
	approx_amount, customer_demand, pechiyamman_demand, in_time, est_time, sign=None
):
	"""
	Generates a Job Card PDF with all details, logo, and unique job card number.
	"""
	from reportlab.lib.pagesizes import A4
	from reportlab.pdfgen import canvas
	from reportlab.lib.units import mm
	from reportlab.lib.utils import ImageReader
	from reportlab.lib import colors
	import os

	pdf_path = os.path.join(os.getcwd(), f"jobcard_{jobcard_number}_{name.replace(' ', '_')}_{phone}.pdf")
	c = canvas.Canvas(pdf_path, pagesize=A4)
	width, height = A4

	margin = 15 * mm
	c.setStrokeColor(colors.darkblue)
	c.setLineWidth(2)
	c.rect(margin, margin, width - 2*margin, height - 2*margin)

	# Logo at top right
	logo_path = os.path.join(os.getcwd(), "img.png")
	if os.path.exists(logo_path):
		c.drawImage(ImageReader(logo_path), width - margin - 40*mm, height - margin - 25*mm, width=35*mm, height=25*mm, preserveAspectRatio=True, mask='auto')

	# Title and Job Card Number
	c.setFont("Helvetica-Bold", 22)
	c.setFillColor(colors.darkblue)
	c.drawCentredString(width/2, height - margin - 10*mm, "NEW JOB CARD")
	c.setFont("Helvetica-Bold", 13)
	c.setFillColor(colors.black)
	c.drawRightString(width - margin - 2*mm, height - margin - 10*mm, f"No: {jobcard_number}")

	# In Time and Est Time
	c.setFont("Helvetica", 11)
	c.drawString(margin + 2*mm, height - margin - 5*mm, f"In Time: {in_time}")
	c.drawString(margin + 80*mm, height - margin - 5*mm, f"Est. Time: {est_time}")

	# Details
	c.setFont("Helvetica", 12)
	y = height - margin - 25*mm
	line_gap = 8*mm
	details = [
		("Name", name),
		("Phone", phone),
		("Place", place),
		("Bike No.", bike_no),
		("Model", model),
		("Year", year),
		("Engine Number", engine_no),
		("Chasis Number", chasis_no),
		("Approx Amount", approx_amount),
	]
	for label, value in details:
		c.drawString(margin + 2*mm, y, f"{label}: {value}")
		y -= line_gap

	# Multi-line fields
	c.setFont("Helvetica-Bold", 12)
	c.drawString(margin + 2*mm, y, "Customer Demand:")
	c.setFont("Helvetica", 12)
	y -= 6*mm
	text_obj = c.beginText(margin + 10*mm, y)
	for line in customer_demand.splitlines():
		text_obj.textLine(line)
		y -= 5*mm
	c.drawText(text_obj)
	y -= 8*mm

	c.setFont("Helvetica-Bold", 12)
	c.drawString(margin + 2*mm, y, "Pechiyamman Demand:")
	c.setFont("Helvetica", 12)
	y -= 6*mm
	text_obj = c.beginText(margin + 10*mm, y)
	for line in pechiyamman_demand.splitlines():
		text_obj.textLine(line)
		y -= 5*mm
	c.drawText(text_obj)
	y -= 12*mm

	# Single Signature heading and space
	c.setFont("Helvetica-Bold", 13)
	c.drawString(margin + 2*mm, margin + 30*mm, "Signature:")
	# Draw a long line for signature space
	c.line(margin + 30*mm, margin + 29*mm, width - margin - 2*mm, margin + 29*mm)

	c.save()
	return pdf_path


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import datetime
import os


def generate_invoice_pdf(name, phone, bike_number, services, total):
	invoice_path = os.path.join(os.getcwd(), f"invoice_{name.replace(' ', '_')}_{phone}.pdf")
	c = canvas.Canvas(invoice_path, pagesize=A4)
	width, height = A4

	# Draw border
	margin = 15 * mm
	c.setStrokeColor(colors.darkblue)
	c.setLineWidth(2)
	c.rect(margin, margin, width - 2*margin, height - 2*margin)

	# Draw logo at top right
	logo_path = os.path.join(os.getcwd(), "img.png")
	if os.path.exists(logo_path):
		c.drawImage(ImageReader(logo_path), width - margin - 40*mm, height - margin - 25*mm, width=35*mm, height=25*mm, preserveAspectRatio=True, mask='auto')

	# Title centered
	c.setFont("Helvetica-Bold", 22)
	c.setFillColor(colors.darkblue)
	c.drawCentredString(width/2, height - margin - 10*mm, "INVOICE / BILL RECEIPT")
	c.setFillColor(colors.black)

	# Date and time (top left, 2 lines)
	now = datetime.now()
	date_str = now.strftime("%d-%m-%Y")
	time_str = now.strftime("%I:%M %p")
	c.setFont("Helvetica", 10)
	c.drawString(margin + 2*mm, height - margin - 5*mm, f"Date: {date_str}")
	c.drawString(margin + 2*mm, height - margin - 11*mm, f"Time: {time_str}")

	# Customer info
	c.setFont("Helvetica", 12)
	c.drawString(margin + 2*mm, height - margin - 35*mm, f"Customer Name: {name}")
	c.drawString(margin + 2*mm, height - margin - 43*mm, f"Phone: {phone}")
	c.drawString(margin + 2*mm, height - margin - 51*mm, f"Bike Number: {bike_number}")

	# Table for services
	table_top = height - margin - 70*mm
	table_left = margin + 2*mm
	table_width = width - 2*margin - 4*mm
	row_height = 12*mm
	col_service = table_left + 2*mm
	col_price = table_left + table_width - 40*mm

	# Table header
	c.setFont("Helvetica-Bold", 13)
	c.setFillColor(colors.white)
	c.setStrokeColor(colors.darkblue)
	c.setLineWidth(1)
	c.setFillColorRGB(0.2, 0.4, 0.8)
	c.roundRect(table_left, table_top, table_width, row_height, 4, fill=1)
	c.setFillColor(colors.white)
	c.drawString(col_service, table_top + 3*mm, "Service")
	c.drawString(col_price, table_top + 3*mm, "Price (₹)")

	# Table rows
	c.setFont("Helvetica", 12)
	c.setFillColor(colors.black)
	y = table_top - row_height
	for service, price in services:
		c.setFillColorRGB(0.95, 0.95, 1)  # light row background
		c.roundRect(table_left, y, table_width, row_height, 2, fill=1, stroke=0)
		c.setFillColor(colors.black)
		c.drawString(col_service, y + 3*mm, service)
		c.drawString(col_price, y + 3*mm, str(price))
		y -= row_height

	# Total row
	c.setFont("Helvetica-BoldOblique", 14)
	c.setFillColorRGB(0.8, 0.9, 1)
	c.roundRect(table_left, y, table_width, row_height, 2, fill=1, stroke=0)
	c.setFillColor(colors.darkblue)
	c.drawString(col_service, y + 3*mm, "Total")
	c.drawString(col_price, y + 3*mm, f"₹{total}")

	# Thank you note
	c.setFont("Helvetica-Oblique", 12)
	c.setFillColor(colors.black)
	c.drawCentredString(width/2, margin + 15*mm, "Thank you for your business!")

	# Footer line
	c.setStrokeColor(colors.lightgrey)
	c.setLineWidth(0.5)
	c.line(margin, margin + 12*mm, width - margin, margin + 12*mm)

	c.save()
