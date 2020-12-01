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
from django.core.files.uploadedfile import InMemoryUploadedFile
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from verifydocs.parameters import WEB_CLIENT_URL, DJ_URL_PROJECT
from security.app import SecurityApp


class PDFTools:
    width = 41
    # width = 61.5
    height = 41
    # height = 61.5

    def __init__(self, pos_x=None, pos_y=None, scale=42):
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.width = float(scale or 42)
        self.height = float(scale or 42)

    def generate_pdf_blanck(self, another_file=None):

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        self.add_img(None, pdf)
        pdf.setTitle('Ejemplo')
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
            for pageNum in range(1, reader.numPages):
                pageObj = reader.getPage(pageNum)
                writer.addPage(pageObj)
            resultFile = open(f'{DJ_URL_PROJECT}/temp/mark.pdf', 'wb')
            writer.write(resultFile)
            resultFile.close()
            pdf = open(f'{DJ_URL_PROJECT}/temp/mark.pdf', 'rb')
            encoded_string = base64.b64encode(pdf.read())
            return encoded_string
        return base64.b64encode(buffer.getvalue())

    def add_watermark(self, original_pdf):
        buffer = BytesIO()
        reader = PdfFileReader(original_pdf)
        page = reader.getPage(0)
        pdf = canvas.Canvas(buffer, pagesize=letter)
        self.add_watermark_img(pdf, page.artBox.upperRight[0],
                               page.artBox.upperRight[1])
        pdf.setTitle('Copia no valida')
        pdf.save()
        buffer.seek(0)
        reader2 = PdfFileReader(buffer)
        waterpage = reader2.getPage(0)
        page.mergePage(waterpage)
        writer = PdfFileWriter()
        writer.addPage(page)
        for pageNum in range(1, reader.numPages):
            pageObj = reader.getPage(pageNum)
            writer.addPage(pageObj)
        resultFile = open(f'{settings.MEDIA_ROOT}/tmp/mark.pdf', 'wb')
        writer.write(resultFile)
        resultFile.close()
        pdf = open(f'{settings.MEDIA_ROOT}/tmp/mark.pdf', 'rb')
        encoded_string = base64.b64encode(pdf.read())
        return encoded_string.decode()

    def add_img(self, img, pdf):
        pdf.drawImage(f'{settings.STATIC_ROOT}/app/rsc/img/QR.png',
                      self.pos_x,
                      self.pos_y, self.width, self.height)
        text = 'Verifique el documento en'
        url = WEB_CLIENT_URL
        self.add_text(pdf, text, self.pos_y-8)
        self.add_text(pdf, url, self.pos_y-16)

    def add_watermark_img(self, pdf, width, height):
        pdf.drawImage(f'{settings.STATIC_ROOT}/app/rsc/img/cnv.png', 0, 0,
                      float(width), float(height), mask='auto')

    def add_text(self, pdf, line, pos_y):
        text_size = stringWidth(line, "Helvetica", 6)
        text = pdf.beginText(self.pos_x + (self.width / 2 - text_size / 2),
                             pos_y)
        text.setFont("Helvetica", 6)
        text.textOut(line)
        pdf.drawText(text)

    def __remove_files_temp(self, ref=None, qr=False):
        patch_media_tmp = f'{settings.MEDIA_ROOT}/tmp'
        os.remove(f'{patch_media_tmp}/{ref}_original.pdf')
        if qr:
            os.remove(f'{patch_media_tmp}/{ref}_out.pdf')
            os.remove(f'{patch_media_tmp}/{ref}.pdf')
            os.remove(f'{patch_media_tmp}/{ref}.svg')

    def __create_pdf_file_qr(self, ref, file):
        try:
            reader = PyPDF2.PdfFileReader(file)
            num_page = reader.getNumPages()
            page = reader.getPage(0)
            water = open(f'{settings.MEDIA_ROOT}/tmp/{ref}.pdf', 'rb')
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

    def __create_file_disk(self, file_doc=None, user=None):
        str_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        ref = f'{str_time}-{user}'
        path = default_storage.save(f'tmp/{ref}_original.pdf',
                                    ContentFile(file_doc.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        file = open(f'{settings.MEDIA_ROOT}/tmp/{ref}_original.pdf', 'rb')

        return ref, file

    def create_main_qr(self, file_doc=None, user=None):
        try:
            ref, file = self.__create_file_disk(file_doc=file_doc, user=user)

            security_app = SecurityApp(pdf_tools=self)
            sha_256, token = security_app.autenticate_document(
                file=file.read(), ref=ref)

            out_file = self.__create_pdf_file_qr(ref=ref, file=file)
            if out_file:
                fv = open(default_storage.path(
                    f'{settings.MEDIA_ROOT}/tmp/{ref}_out.pdf'), 'rb')
                stream_str = io.BytesIO(fv.read())
                text_file = InMemoryUploadedFile(
                    stream_str, 'file_qr', f'{file_doc}', 'application/pdf',
                    stream_str.getvalue().__sizeof__(), None, dict()
                )
                self.__remove_files_temp(ref=ref, qr=True)
                return text_file, sha_256, token
        except Exception as e:
            print(e)
            print('create_main_qr')
            return None

    def create_hash_qr(self, file_doc, user=None):
        ref, file = self.__create_file_disk(file_doc=file_doc, user=user)
        security_app = SecurityApp(pdf_tools=self)
        self.__remove_files_temp(ref=ref)
        return security_app.create_hash_256_qr(file=file.read()), io.BytesIO(file.read()).getvalue()

    def get_hash_document(self, file_doc, user):
        ref = ''
        try:
            ref, file = self.__create_file_disk(file_doc=file_doc, user=user)
            # io.BytesIO(file.read())
            return SecurityApp(None).create_hash_256_qr(file=file.read())
        finally:
            if ref:
                self.__remove_files_temp(ref)


def create_pdf(text='blank'):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle('blank')
    pdf.drawString(100, 100, text)
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()
