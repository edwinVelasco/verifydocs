import base64
from io import BytesIO

from PyPDF2 import PdfFileReader, PdfFileWriter
from django.conf import settings
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


class PDFTools:
    width = 41
    height = 41

    def __init__(self, pos_x, pos_y):
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)

    def generate_pdf_blanck(self, another_file=None):

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        self.add_img(None, pdf)
        pdf.save()
        if another_file:
            buffer.seek(0)
            reader = PdfFileReader(another_file)
            page = reader.getPage(0)
            reader2 = PdfFileReader(buffer)
            waterpage = reader2.getPage(0)
            page.mergePage(waterpage)
            writer = PdfFileWriter()
            writer.addPage(page)
            print('num de pags', reader.numPages)
            for pageNum in range(1, reader.numPages):
                pageObj = reader.getPage(pageNum)
                writer.addPage(pageObj)
            resultFile = open(f'temp/mark.pdf', 'wb')
            writer.write(resultFile)
            resultFile.close()
            pdf = open('temp/mark.pdf', 'rb')
            encoded_string = base64.b64encode(pdf.read())
            return encoded_string
        return base64.b64encode(buffer.getvalue())


    def add_img(self, img, pdf):
        pdf.drawImage(f'{settings.STATIC_ROOT}/app/rsc/img/QR.png',
                      self.pos_x,
                      self.pos_y, self.width, self.height)
        text = 'Verifique el documento en'
        url = 'https://albertove.pythonanywhere.com'
        self.add_text(pdf, text, self.pos_y-8)
        self.add_text(pdf, url, self.pos_y-16)

    def add_text(self, pdf, line, pos_y):
        text_size = stringWidth(line, "Helvetica", 6)
        text = pdf.beginText(self.pos_x + (self.width / 2 - text_size / 2),
                             pos_y)
        text.setFont("Helvetica", 6)
        text.textOut(line)
        pdf.drawText(text)