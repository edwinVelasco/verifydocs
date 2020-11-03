import base64
import os
import io
import datetime
import pyqrcode
from io import BytesIO
import PyPDF2
import hashlib
import base64
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from verifydocs.parameters import WEB_CLIENT_URL, DJ_URL_PROJECT


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
        url = WEB_CLIENT_URL
        self.__add_text(pdf, text, self.pos_y-8)
        self.__add_text(pdf, url, self.pos_y-16)

    def __add_text(self, pdf, line, pos_y):
        text_size = stringWidth(line, "Helvetica", 6)
        text = pdf.beginText(self.pos_x + (self.width / 2 - text_size / 2),
                             pos_y)
        text.setFont("Helvetica", 6)
        text.textOut(line)
        pdf.drawText(text)

    def hash(self, file_base64=None):
        try:
            sha_512 = hashlib.sha512(file_base64)
            # print(sha_512.hexdigest())
            sha_256 = hashlib.sha256(sha_512.digest())
            # print(sha_256.hexdigest())
            # md_5 = hashlib.md5(sha_256.digest())
            return sha_256
        except Exception as e:
            print(e)
            print('hash')
            return None

    def __createQR(self, file=None, ref=None):
        try:
            file = base64.b64encode(file)
            sha_256 = self.hash(file_base64=file)
            md_5 = hashlib.md5(sha_256.digest())

            qr2 = pyqrcode.create(md_5.hexdigest())
            qr2.svg(f'{DJ_URL_PROJECT}/temp/{ref}.svg', scale=1)
            my_canvas = canvas.Canvas(f'{DJ_URL_PROJECT}/temp/{ref}.pdf',
                                      pagesize=letter)
            drawing = svg2rlg(f'{DJ_URL_PROJECT}/temp/{ref}.svg')
            renderPDF.draw(drawing, my_canvas, self.pos_x, self.pos_y)
            self.__add_text(my_canvas, 'Verifique el documento en',
                            self.pos_y - 8)
            self.__add_text(my_canvas, WEB_CLIENT_URL, self.pos_y - 16)
            my_canvas.save()
            return ref, sha_256.hexdigest(), md_5.hexdigest()
        except Exception as e:
            print(e)
            print('__createQR')
            return None

    def __create_pdf_file_qr(self, ref, file):
        try:
            reader = PyPDF2.PdfFileReader(file)
            page = reader.getPage(0)
            water = open(f'{DJ_URL_PROJECT}/temp/{ref}.pdf', 'rb')
            reader2 = PyPDF2.PdfFileReader(water)
            waterpage = reader2.getPage(0)
            page.mergePage(waterpage)
            writer = PyPDF2.PdfFileWriter()
            writer.addPage(page)
            for pageNum in range(1, reader.numPages):
                pageObj = reader.getPage(pageNum)
                writer.addPage(pageObj)
            resultFile = open(f'{settings.MEDIA_ROOT}/tmp/{ref}_out.pdf', 'wb')
            writer.write(resultFile)
            resultFile.close()
            return True
        except Exception as e:
            print(e)
            print('__create_pdf_file_qr')
            return None

    def create_pdf_watermark(self, file):
        reader = PyPDF2.PdfFileReader(file)
        page = reader.getPage(0)
        water = open('tools/watermark_page.pdf', 'rb')
        reader2 = PyPDF2.PdfFileReader(water)

        waterpage = reader2.getPage(0)
        # waterpage.mergePage(page)
        page.mergePage(waterpage)
        writer = PyPDF2.PdfFileWriter()
        # writer.addPage(waterpage)
        writer.addPage(page)
        for pageNum in range(1,
                             reader.numPages):  # this will give length of book
            pageObj = reader.getPage(pageNum)
            writer.addPage(pageObj)
        ref = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        resultFile = open(f'{DJ_URL_PROJECT}/temp/{ref}_watermark_out.pdf',
                          'wb')

        writer.write(resultFile)
        # resultFile.close()
        return resultFile

    def create_main_qr(self, file_doc):
        ref = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        path = default_storage.save(f'tmp/{ref}_original.pdf',
                                    ContentFile(file_doc.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        file = open(f'{settings.MEDIA_ROOT}/tmp/{ref}_original.pdf', 'rb')
        ref, sha_256, token = self.__createQR(file=file.read(), ref=ref)
        out_file = self.__create_pdf_file_qr(ref=ref, file=file)
        if out_file:
            # out_file = open(f'{DJ_URL_PROJECT}/temp/{ref}_out.pdf', 'rb').read()
            fv = open(default_storage.path(
                f'{settings.MEDIA_ROOT}/tmp/{ref}_out.pdf'), 'rb').read()
            stream_str = io.BytesIO(fv)
            text_file = InMemoryUploadedFile(
                stream_str, 'file_qr', f'{file_doc}', 'application/pdf', stream_str.getvalue().__sizeof__(), None
            )
            return text_file, sha_256, token








