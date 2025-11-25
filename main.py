import os
import sqlite3
import logging
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# --- Import Views (Screens) ---
# These will be created in later steps.
# Ensuring these imports exist effectively registers them with Kivy if they define KV rules.
from screens.dashboard import DashboardScreen
from screens.stock_add import StockAddScreen
from screens.stock_list import StockListScreen
from screens.billing import BillingScreen
from screens.jobcard import JobCardScreen
from screens.analytics import AnalyticsScreen
from screens.customer_list import CustomerListScreen
from screens.vehicle_list import VehicleListScreen

# --- Import Backend Configurations ---
from firebase.firebase_config import initialize_firebase
from local_storage.db_init import initialize_local_db

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkshopWindowManager(ScreenManager):
    """
    The main manager that handles navigation between different screens.
    """

    pass


class WorkshopApp(App):
    """
    Main Application Class for the Workshop Management App.
    """

    def build(self):
        # 1. Set Window properties (Optional: good for testing on PC)
        # Window.size = (360, 800) # Typical Android phone aspect ratio

        # 2. Initialize Databases
        self._setup_databases()

        # 3. Load the KV file explicitly (if name doesn't match App name)
        # Kivy auto-loads 'workshop.kv' if App is WorkshopApp, but we use app.kv
        kv_file_path = os.path.join(os.path.dirname(__file__), "app.kv")
        Builder.load_file(kv_file_path)

        # 4. Return the ScreenManager
        return WorkshopWindowManager()

    def _setup_databases(self):
        """
        Handles the initialization of Firebase (Online) and SQLite (Offline).
        """
        try:
            # Initialize Local SQLite
            # We will define initialize_local_db in the local_storage module later
            initialize_local_db()
            logger.info("SQLite Local DB initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to init SQLite: {e}")

        try:
            # Initialize Firebase
            # We will define initialize_firebase in firebase/firebase_config.py later
            initialize_firebase()
            logger.info("Firebase initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to init Firebase (App might be offline): {e}")


if __name__ == "__main__":
    WorkshopApp().run()
