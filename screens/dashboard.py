from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.factory import Factory
from datetime import datetime


class DashboardScreen(Screen):
    def on_enter(self, *args):
        """
        Called when the screen is displayed.
        We use schedule_once to wait 1 frame ensuring IDs are loaded.
        """
        Clock.schedule_once(self.update_time, 0)
        Clock.schedule_once(self.update_shop_info, 0)
        self.clock_event = Clock.schedule_interval(self.update_time, 1)

    def on_leave(self, *args):
        """
        Called when leaving the screen.
        Stops the clock to save battery.
        """
        if self.clock_event:
            self.clock_event.cancel()

    def update_shop_info(self, *args):
        """Updates the shop name - you can load this from settings/database"""
        if "shop_name_label" in self.ids:
            # Replace this with your actual workshop name
            self.ids.shop_name_label.text = "Pechiyamman Auto Service Zone"

    def update_time(self, *args):
        """Updates the separate date and time labels."""
        # Safety check: if the screen isn't fully built yet, stop.
        if "date_label" not in self.ids:
            return

        now = datetime.now()

        # Left Box: Date
        current_date = now.strftime("%d %B %Y")
        self.ids.date_label.text = f"Date: {current_date}"

        # Right Box: Time
        current_time = now.strftime("%I:%M %p")
        self.ids.time_label.text = f"Time: {current_time}"

    def open_service_popup(self):
        Factory.ServicePopup().open()

    def open_billing_popup(self):
        Factory.BillingPopup().open()
