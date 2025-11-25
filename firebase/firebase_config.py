import firebase_admin
from firebase_admin import credentials, firestore
import os

# Global DB client
db = None


def initialize_firebase():
    """
    Initializes the connection to Firebase Firestore.
    If the key file is missing, it skips initialization (Offline Mode).
    """
    global db

    # Path to the JSON key file
    cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

    # Check if key exists
    if not os.path.exists(cred_path):
        print("---------------------------------------------------")
        print(f"WARNING: Firebase Key not found at: {cred_path}")
        print("App will run in OFFLINE ONLY mode.")
        print("---------------------------------------------------")
        return None

    try:
        # Avoid initializing twice
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("SUCCESS: Connected to Firebase Firestore.")
        return db
    except Exception as e:
        print(f"ERROR: Failed to initialize Firebase: {e}")
        return None
