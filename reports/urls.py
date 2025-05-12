from django.urls import path
from .views import HTMLReportView, HTMLReportStatusView, PDFReportView, PDFReportStatusView

urlpatterns = [
    path('assignment/html', HTMLReportView.as_view(), name='html-report'),
     path('assignment/html/<uuid:task_id>', HTMLReportStatusView.as_view(), name='html-report-status'),
     path('assignment/pdf', PDFReportView.as_view(), name='pdf-report'),
     path('assignment/pdf/<uuid:task_id>', PDFReportStatusView.as_view()),
]

