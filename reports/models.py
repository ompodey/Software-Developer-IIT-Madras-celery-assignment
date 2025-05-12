from django.db import models
import uuid

class ReportTask(models.Model): #Base Model
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.CharField(max_length=64)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('STARTED', 'Started'), ('SUCCESS', 'Success'), ('FAILURE', 'Failure')],
        default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

class HTMLReport(ReportTask): #HTML Report Model
    content = models.TextField()  # PostgreSQL handles large text efficiently

class PDFReport(ReportTask):
    #Stores PDF reports using binary field.
    content = models.BinaryField(null=True, blank=True)  # For storing PDF binary data
    file_size = models.IntegerField(null=True, blank=True)  # Track size for optimization
