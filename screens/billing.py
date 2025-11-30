from kivy.uix.screenmanager import Screen

from utils.pdf_generator import generate_invoice_pdf
from utils.google_sheets_logger import create_monthly_sheet_and_append

class BillingScreen(Screen):
    def generate_invoice(self, name, phone, bike_number, bike_wash, car_wash, bike_repairs, car_repairs):
        services = []
        total = 0
        if bike_wash:
            services.append(("Bike wash", 100))
            total += 100
        if car_wash:
            services.append(("Car wash", 300))
            total += 300
        if bike_repairs:
            services.append(("Bike repairs", 200))
            total += 200
        if car_repairs:
            services.append(("Car repair", 2000))
            total += 2000

        # Call PDF generator utility
        generate_invoice_pdf(name, phone, bike_number, services, total)

        # After invoice is generated:
        invoice_row = [[name, phone, bike_number, total]]
        create_monthly_sheet_and_append(invoice_row)
