from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.models import auth # type: ignore
from django.contrib import messages # type: ignore
from django.http import JsonResponse
from .models import Chatroom
from .ai.report_generation import process_sales_analysis
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings  
from django.http import FileResponse, HttpResponseNotFound ,HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from markdownify.templatetags.markdownify import markdownify
from .ai.churnpredict import predictions
import os
import json 

# Create your views here.

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')  
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')  


def logout(request):
    auth.logout(request)
    return redirect('/')


def chatquery(request):
    return render(request,'chatquery.html')


def get_user_room(request):
    user_id=request.session.session_key or request.user.id
    room,_=Chatroom.objects.get_or_create(room_name=f"user_{user_id}")
    return JsonResponse({"room_name":room.room_name})




@csrf_exempt
def sales_summariser(request):
    if request.method == "POST":
        response = process_sales_analysis()
        cleaned_content = response.strip('```json\n').strip("```")

        try:
            data = json.loads(cleaned_content)
        except json.JSONDecodeError:
            return render(request, "sales_summary.html", {
                "error": "Invalid JSON response",
                "displayGraph": False
            })

        json_data = data["json_data"]
        summary = markdownify(data["summary"])


        weekly_sales_data = {
            "type": "bar",
            "data": {
                "labels": list(json_data["weekly_sales_trends"]["sales_by_category"].keys()),
                "datasets": [{
                    "label": "Weekly Sales",
                    "data": list(json_data["weekly_sales_trends"]["sales_by_category"].values()),
                    "backgroundColor": "#4e73df"
                }]
            }
        }

        monthly_sales_data = {
            "type": "bar",
            "data": {
                "labels": list(json_data["monthly_sales_trends"]["sales_by_category"].keys()),
                "datasets": [{
                    "label": "Monthly Sales",
                    "data": list(json_data["monthly_sales_trends"]["sales_by_category"].values()),
                    "backgroundColor": "#1cc88a"
                }]
            }
        }

        yearly_sales_data = {
            "type": "bar",
            "data": {
                "labels": list(json_data["yearly_sales_trends"]["sales_by_category"].keys()),
                "datasets": [{
                    "label": "Yearly Sales",
                    "data": list(json_data["yearly_sales_trends"]["sales_by_category"].values()),
                    "backgroundColor": "#36b9cc"
                }]
            }
        }

        region_sales_data = {
            "type": "pie",
            "data": {
                "labels": list(json_data["yearly_sales_trends"]["sales_by_region"].keys()),
                "datasets": [{
                    "label": "Sales by Region",
                    "data": list(json_data["yearly_sales_trends"]["sales_by_region"].values()),
                    "backgroundColor": [
                        "#f6c23e", "#e74a3b", "#858796", "#1cc88a"
                    ]
                }]
            }
        }

        context = {
            "summary": summary,
            "displayGraph": True,
            "weekly_sales_data": json.dumps(weekly_sales_data),
            "monthly_sales_data": json.dumps(monthly_sales_data),
            "yearly_sales_data": json.dumps(yearly_sales_data),
            "region_sales_data": json.dumps(region_sales_data)
        }

        file_path = os.path.join(settings.MEDIA_ROOT, 'sales_report.pdf')
        generate_pdf(summary, file_path)

        return render(request, "sales_summary.html", context)

    return render(request, "sales_summary.html", {"displayGraph": False})

def download_pdf(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'sales_report.pdf')
    
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    return HttpResponseNotFound('PDF not found yet. Please generate it first.')

def generate_pdf(report_data, filename):
    """Generate PDF using ReportLab"""
  
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []
    
    title = Paragraph("Sales Analysis Report", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 12))
    
    if isinstance(report_data, dict):
        text = report_data.get('summary', 'No analysis available')
    else:
        text = str(report_data)
        
    body = Paragraph(text, styles['BodyText'])
    content.append(body)
    
    doc.build(content)


@csrf_exempt
def run_churn_prediction(request):
    if request.method == "POST":
        try:
            result = predictions()  # Call the function that returns the churn prediction data
            return render(request, "churn_results.html", {"notifications": result})
        except Exception as e:
            return render(request, "churn_results.html", {"error": f"Error: {str(e)}"})
    return render(request, "churn_results.html")

# def run_churn_prediction(request):
#     if request.method == 'POST':
#         try:
#             results = predictions()  # your Celery task or function call
#             return JsonResponse({"status": "success", "data": results})
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=500)
#     return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)