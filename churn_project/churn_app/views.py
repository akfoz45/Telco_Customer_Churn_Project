import json
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from .models import Customer, ChurnPrediction

@csrf_exempt
def predict_churn(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            ml_model = apps.get_app_config('churn_app').ml_model
            
            if ml_model is None:
                return JsonResponse({'error': 'No machine learning model was found.'}, status=500)
            
            df = pd.DataFrame([data])
            
            churn_prob = ml_model.predict_proba(df)[0][1]
            churn_prob_percentage = round(churn_prob * 100, 2)
            
            is_high_risk = churn_prob_percentage >= 70.0
            
            customer, created = Customer.objects.update_or_create(
                id=data.get('id', None),
                defaults={
                    'gender': data.get('gender', ''),
                    'senior_citizen': int(data.get('SeniorCitizen', 0)),
                    'partner': data.get('Partner', ''),
                    'dependents': data.get('Dependents', ''),
                    'tenure': int(data.get('tenure', 0)),
                    'phone_service': data.get('PhoneService', ''),
                    'multiple_lines': data.get('MultipleLines', ''),
                    'internet_service': data.get('InternetService', ''),
                    'online_security': data.get('OnlineSecurity', ''),
                    'online_backup': data.get('OnlineBackup', ''),
                    'device_protection': data.get('DeviceProtection', ''),
                    'tech_support': data.get('TechSupport', ''),
                    'streaming_tv': data.get('StreamingTV', ''),
                    'streaming_movies': data.get('StreamingMovies', ''),
                    'contract': data.get('Contract', ''),
                    'paperless_billing': data.get('PaperlessBilling', ''),
                    'payment_method': data.get('PaymentMethod', ''),
                    'monthly_charges': float(data.get('MonthlyCharges', 0.0)),
                    'total_charges': float(data.get('TotalCharges', 0.0)),
                }
            )
            
            ChurnPrediction.objects.update_or_create(
                customer=customer,
                defaults={
                    'churn_probability': churn_prob_percentage,
                    'is_high_risk': is_high_risk,
                }
            )
            
            response_data = {
                'status': 'success',
                'customer_id': customer.id,
                'churn_probability': churn_prob_percentage,
                'is_high_risk': is_high_risk,
                'message': 'The risk of failure is high. Should this customer be given a %15 renewal discount via SMS?' if is_high_risk else 'Customer profile is stable. Risk is low.'
            }
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request method. Only POST is supported.'}, status=405)