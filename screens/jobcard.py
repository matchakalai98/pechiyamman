from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App
import utils.pdf_generator as pdfgen
import re  # Import regex for validation
import os  # Import os for file handling


class JobCardScreen(Screen):
    def generate_job_card_pdf(
        self,
        name,
        phone,
        place,
        bike_no,
        model,
        year,
        engine_no,
        chassis_no,
        approx_amount,
        customer_demand,
        pechiyamman_demand,
        in_time,
        est_time,
    ):
        # Basic validation
        if not name or not phone or not bike_no:
            self.show_popup("Error", "Name, Phone, and Bike No. are required.")
            return

        # Phone validation: 10-14 characters, only digits, +, and -
        if not re.fullmatch(r"[0-9+\-]{10,14}", phone):
            self.show_popup(
                "Error",
                "Phone number must be 10-14 characters long and can only contain digits, +, and -.",
            )
            return

        # Bike No. validation: Format XY60AB1234 or XY20C1234
        if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z]{0,2}\d{1,4}", bike_no):
            self.show_popup(
                "Error",
                "Bike No. must be in the format XX00XX0000 (e.g., TN01AB1234, MH12C5678).",
            )
            return

        # Year validation: Only numbers allowed
        if not year.isdigit():
            self.show_popup("Error", "Year must contain only numbers.")
            return

        # Approx Amount validation: Append ₹ symbol if not present
        if not approx_amount.startswith("₹"):
            approx_amount = f"₹{approx_amount}"

        # Get and increment job card number
        counter_file = "jobcard_counter.txt"
        try:
            if not os.path.exists(counter_file):
                jobcard_number = 1
            else:
                with open(counter_file, "r") as f:
                    jobcard_number = int(f.read().strip()) + 1
        except Exception:
            jobcard_number = 1
        # Save the new number
        try:
            with open(counter_file, "w") as f:
                f.write(str(jobcard_number))
        except Exception:
            pass

        # Generate PDF with job card number
        pdf_path = pdfgen.generate_job_card_pdf(
            jobcard_number,
            name,
            phone,
            place,
            bike_no,
            model,
            year,
            engine_no,
            chassis_no,
            approx_amount,
            customer_demand,
            pechiyamman_demand,
            in_time,
            est_time,
        )
        self.show_popup(
            "Success", f"Job Card #{jobcard_number} PDF generated:\n{pdf_path}"
        )

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.3))
        popup.open()



