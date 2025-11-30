
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App
import utils.pdf_generator as pdfgen

class JobCardScreen(Screen):
    def generate_job_card_pdf(self, name, phone, place, bike_no, model, year, engine_no, chasis_no, approx_amount, customer_demand, pechiyamman_demand, in_time, est_time):
        # Basic validation
        if not name or not phone or not bike_no:
            self.show_popup("Error", "Name, Phone, and Bike No. are required.")
            return

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
            jobcard_number, name, phone, place, bike_no, model, year, engine_no, chasis_no,
            approx_amount, customer_demand, pechiyamman_demand, in_time, est_time
        )
        self.show_popup("Success", f"Job Card #{jobcard_number} PDF generated:\n{pdf_path}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.3))
        popup.open()

# --- App methods for time and datetime picker ---
class MainApp(App):
    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%d-%m-%Y %I:%M %p")

    def open_datetime_picker(self, textinput):
        # Placeholder: Implement a proper datetime picker popup if needed
        # For now, just set current time for demonstration
        from datetime import datetime
        textinput.text = datetime.now().strftime("%d-%m-%Y %I:%M %p")
