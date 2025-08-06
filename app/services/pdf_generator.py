from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

class PDFGenerator:
    @staticmethod
    def generate_pdf(content, filename="document.pdf"):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Set up styles
        c.setFont("Helvetica", 12)
        y_position = height - 40
        
        # Add content with proper formatting
        for line in content.split('\n'):
            if y_position < 40:
                c.showPage()
                y_position = height - 40
                c.setFont("Helvetica", 12)
            c.drawString(40, y_position, line)
            y_position -= 15
        
        c.save()
        buffer.seek(0)
        return buffer