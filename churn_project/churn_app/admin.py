from django.contrib import admin
from .models import Customer, ChurnPrediction

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "gender", "contract", "tenure", "monthly_charges", "total_charges")
    search_fields = ("id", "cotract")
    list_filter = ("contract", "internet_service", "payment_method")

@admin.register(ChurnPrediction)
class ChurnPredictionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'churn_probability', 'is_high_risk', 'action_taken', 'created_at')
    list_filter = ('is_high_risk', 'action_taken')
    search_fields = ('customer__id',)