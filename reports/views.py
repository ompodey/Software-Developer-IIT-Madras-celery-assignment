from rest_framework.views import APIView # Django REST Framework
from rest_framework.response import Response 
from rest_framework import status
from django.http import HttpResponse
from .serializers import EventDataSerializer 
from .tasks import generate_html_report, generate_pdf_report # Celery tasks
from .models import HTMLReport, PDFReport # Django models
import uuid      

class HTMLReportStatusView(APIView):
    def get(self, request, task_id):
        try:
            report = HTMLReport.objects.get(task_id=task_id)
        except HTMLReport.DoesNotExist:
            return Response({"error": "Task not found"},
                          status=status.HTTP_404_NOT_FOUND)
        
        if report.status == 'SUCCESS':
            # Return the HTML content directly for display
            return HttpResponse(report.content, content_type='text/html')
        
        # For other statuses, return JSON response
        response_data = {
            "status": report.status,
            "student_id": report.student_id,
            "created_at": report.created_at,
            "updated_at": report.updated_at
        }
        
        if report.status == 'FAILURE':
            response_data['error'] = report.error_message

        return Response(response_data)

class HTMLReportView(APIView):
    def post(self, request):
        serializer = EventDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Generate a UUID for task_id before queuing the task
        task_id = str(uuid.uuid4())

        HTMLReport.objects.create(
            task_id=task_id,
            student_id=serializer.validated_data['student_id'],
            status='RUNNING'
        )
        # Pass task_id explicitly to Celery
        generate_html_report.apply_async(
            args=[serializer.validated_data],
            task_id=task_id
        )

        return Response({"task_id": task_id}, status=status.HTTP_202_ACCEPTED)




class PDFReportView(APIView):
    def post(self, request):
        serializer = EventDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Generate a UUID for task_id before queuing the task
        task_id = str(uuid.uuid4())

        # Create the DB entry with status = RUNNING
        PDFReport.objects.create(
            task_id=task_id,
            student_id=serializer.validated_data['student_id'],
            status='RUNNING'
        )

        # Pass task_id explicitly to Celery
        generate_pdf_report.apply_async(
            args=[serializer.validated_data],
            task_id=task_id  
        )

        return Response({"task_id": task_id}, status=status.HTTP_202_ACCEPTED)




class PDFReportStatusView(APIView):
    def get(self, request, task_id):
        try:
            report = PDFReport.objects.get(task_id=task_id)
        except PDFReport.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        # If the report is successful, return the PDF content
        if report.status == 'SUCCESS':
            response = HttpResponse(report.content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{report.student_id}.pdf"'
            response['Content-Length'] = report.file_size
            return response

        response_data = {
            "status": report.status,
            "student_id": report.student_id,
            "created_at": report.created_at,
            "updated_at": report.updated_at,
        }

        if report.status == 'FAILURE':
            response_data['error'] = report.error_message

        return Response(response_data)