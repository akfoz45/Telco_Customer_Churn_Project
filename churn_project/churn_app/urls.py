from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/predict/", views.predict_churn, name="predict_churn"),
    path("api/apply-campaign/", views.apply_campaign, name="apply_campaign"),
]