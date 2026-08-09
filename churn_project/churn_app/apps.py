from django.apps import AppConfig
from django.conf import settings
import os
import pickle


class ChurnAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'churn_app'
    ml_model = None

    def ready(self):
        model_path = os.path.join(settings.BASE_DIR, "churn_app", "ml_model", "model.pkl")

        if os.path.exists(model_path):
            with open(model_path, "rb") as file:
                self.ml_model = pickle.load(file)
            print("The Machine Learning Model (model.pkl) has been successfully loaded!")
        else:
            print(f"Warning: Model file not found! Please check: {model_path}")