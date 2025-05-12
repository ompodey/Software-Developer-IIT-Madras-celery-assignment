from celery import shared_task
from .models import HTMLReport, PDFReport
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from textwrap import wrap
@shared_task(bind=True, max_retries=3)
def generate_html_report(self, event_data):
    try:
        student_id = event_data['student_id']
        
        # Convert units to integers for proper numeric sorting
        processed_events = []
        for event in event_data['events']:
            unit = event['unit']
            try:
                processed_events.append({
                    **event,
                    'unit': int(unit) if isinstance(unit, str) and unit.isdigit() else unit
                })
            except (ValueError, AttributeError):
                processed_events.append(event)

        # Sort unique units numerically (strings come after numbers)
        unique_units = sorted(
            {event['unit'] for event in processed_events},
            key=lambda x: int(x) if str(x).isdigit() else float('inf')
        )
        
        # Create mapping using original unit values
        unit_mapping = {
            str(unit): f"Q{i+1}" 
            for i, unit in enumerate(unique_units)
        }
        
        # Generate event order with original units
        event_order = " -> ".join([
            unit_mapping.get(str(event['unit']), f"[{event['unit']}]") 
            for event in event_data['events']  # Use original events for order
        ])

        # Update existing DB entry (removed text wrapping)
        HTMLReport.objects.filter(task_id=self.request.id).update(
            status='SUCCESS',
            content=f"""
                <h2>Student ID: {student_id}</h2>
                <p>Event Order: {event_order}</p>
            """
        )
        return str(self.request.id)

    except Exception as e:
        HTMLReport.objects.filter(task_id=self.request.id).update(
            status='FAILURE',
            error_message=str(e)
        )
        raise self.retry(exc=e)

@shared_task(bind=True, max_retries=3)
def generate_pdf_report(self, event_data):
    try:
        student_id = event_data['student_id']
        
        # Convert units to integers for proper numeric sorting
        processed_events = []
        for event in event_data['events']:
            unit = event['unit']
            try:
                processed_events.append({
                    **event,
                    'unit': int(unit) if isinstance(unit, str) and unit.isdigit() else unit
                })
            except (ValueError, AttributeError):
                processed_events.append(event)

        # Sort unique units numerically (strings come after numbers)
        unique_units = sorted(
            {event['unit'] for event in processed_events},
            key=lambda x: int(x) if str(x).isdigit() else float('inf')
        )
        
        # Create mapping using original unit values
        unit_mapping = {
            str(unit): f"Q{i+1}" 
            for i, unit in enumerate(unique_units)
        }
        
        # Generate event order with original units
        event_order = " -> ".join([
            unit_mapping.get(str(event['unit']), f"[{event['unit']}]") 
            for event in event_data['events']  # Use original events for order
        ])

        # Prepare PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Static details
        p.drawString(100, 750, f"Student ID: {student_id}")

        # Wrap the long string into lines
        wrapped_lines = wrap(f"Event Order: {event_order}", width=70)
        y_position = 730
        for line in wrapped_lines:
            p.drawString(100, y_position, line)
            y_position -= 20  # Line spacing

            # New page if needed
            if y_position < 100:
                p.showPage()
                y_position = 750

        p.showPage()
        p.save()

        pdf_content = buffer.getvalue()
        buffer.close()

        # Update existing report entry
        PDFReport.objects.filter(task_id=self.request.id).update(
            status='SUCCESS',
            content=pdf_content,
            file_size=len(pdf_content)
        )

        return str(self.request.id)

    except Exception as e:
        PDFReport.objects.filter(task_id=self.request.id).update(
            status='FAILURE',
            error_message=str(e)
        )
        raise self.retry(exc=e)