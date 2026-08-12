import json
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.shortcuts import render
from .models import Customer, ChurnPrediction

@csrf_exempt
def predict_churn(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_id = data.get("id")

            customer = Customer.objects.get(id=customer_id)

            model_data = {
                "gender": customer.gender,
                "SeniorCitizen": customer.senior_citizen,
                "Partner": customer.partner,
                "Dependents": customer.dependents,
                "tenure": customer.tenure,
                "PhoneService": customer.phone_service,
                "MultipleLines": customer.multiple_lines,
                "InternetService": customer.internet_service,
                "OnlineSecurity": customer.online_security,
                "OnlineBackup": customer.online_backup,
                "DeviceProtection": customer.device_protection,
                "TechSupport": customer.tech_support,
                "StreamingTV": customer.streaming_tv,
                "StreamingMovies": customer.streaming_movie, 
                "Contract": customer.contract,
                "PaperlessBilling": customer.paperless_billing,
                "PaymentMethod": customer.payment_method,
                "MonthlyCharges": customer.monthly_charges,
                "TotalCharges": customer.total_charges
            }

            ml_model = apps.get_app_config("churn_app").ml_model
            if ml_model is None:
                return JsonResponse({'error': 'No machine learning model was found.'}, status=500)

            df = pd.DataFrame([model_data])

            churn_prob = ml_model.predict_proba(df)[0][1]
            churn_prob_percentage = float(round(churn_prob * 100, 2))

            is_high_risk = bool(churn_prob_percentage >= 70.0)

            ChurnPrediction.objects.update_or_create(
                customer=customer,
                defaults={
                    'churn_probability': churn_prob_percentage,
                    'is_high_risk': is_high_risk,
                }
            )

            response_data = {
                "status": "success",
                "customer_id": customer.id,
                'churn_probability': churn_prob_percentage,
                'is_high_risk': is_high_risk,
                'message': 'The risk of failure is high. Should this customer be given a %15 renewal discount via SMS?' if is_high_risk else 'Customer profile is stable. Risk is low.'
            }
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method. Only POST is supported.'}, status=405)

def dashboard(request):
    customers = Customer.objects.all().order_by("-id")[:50]
    return render(request, 'churn_app/dashboard.html', {'customers': customers})

@csrf_exempt
def apply_campaign(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            customer_id = data.get("customer_id")

            prediction = ChurnPrediction.objects.get(customer__id=customer_id)
            prediction.action_taken = True
            prediction.save()

            return JsonResponse({'status': 'success', 'message': 'The campaign has been successfully completed!'})
        except ChurnPrediction.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Customer estimate not found."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST is supported."}, statuse=405)