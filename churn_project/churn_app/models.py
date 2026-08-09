from django.db import models

class Customer(models.Model):
    gender = models.CharField(max_length=10, verbose_name="Gender")
    senior_citizen = models.IntegerField(verbose_name="elderly customer")
    partner = models.CharField(max_length=10, verbose_name="Does he/she have a partner?")
    dependents = models.CharField(max_length=10, verbose_name="Person Responsible for Caring")
    tenure = models.IntegerField(verbose_name="Customer Duration (Months)")
    phone_service = models.CharField(max_length="10", verbose_name="Phone Service")
    multiple_lines = models.CharField(max_length=10, verbose_name="Multiple Lines")
    internet_service = models.CharField(max_length=30, verbose_name="Internet Service")
    online_security = models.CharField(max_length=10, verbose_name="Online Security")
    online_backup = models.CharField(max_length=10, verbose_name="Online Backup")
    device_protection = models.CharField(max_length=10, verbose_name="Device Protection")
    tech_support = models.CharField(max_length=10, verbose_name="Tech Support")
    streaming_tv = models.CharField(max_length=10, verbose_name="Streaming TV")
    streaming_movie = models.CharField(max_length=10, verbose_name="Streamin Movie")
    contract = models.CharField(max_length=30, verbose_name="Contract Type")
    paperless_billing = models.CharField(max_length=10, verbose_name="Paperless Billing")
    payment_method = models.CharField(max_length=50, verbose_name="Payment Method")
    monthly_charges = models.FloatField(verbose_name="Monthly Charges")
    total_charges = models.FloatField(verbose_name="Total Charges")

    def __str__(self):
        return f"Customer #{self.id} - {self.contract} ({self.tenure} Months)"

class ChurnPrediction(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="prediction")
    churn_probability = models.FloatField(verbose_name="Probability of Churning (%)")
    is_high_risk = models.BooleanField(default=False, verbose_name="High Risk?")
    action_taken = models.BooleanField(default=False, verbose_name="Was the campaign implemented?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Estimated Date")

    def __str__(self):
        return f"Customer #{self.customer.id} Estimated - Risk: %{self.churn_probability}"