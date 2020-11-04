import pyqrcode
import hashlib
import base64

from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import letter

from django.conf import settings

from verifydocs.parameters import WEB_CLIENT_URL


class SecurityApp:
    def __init__(self, pdf_tools):
        self.pdf_tools = pdf_tools

    def __encrypt_document_sha256(self, file_base64=None):
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

    def __encrypt_sha256_to_md5(self, sha_256=None):
        return hashlib.md5(sha_256.digest()).hexdigest()

    def autenticate_document(self, file=None, ref=None):
        try:
            file = base64.b64encode(file)
            sha_256 = self.__encrypt_document_sha256(file_base64=file)
            md_5 = self.__encrypt_sha256_to_md5(sha_256=sha_256)

            qr2 = pyqrcode.create(md_5)
            qr2.svg(f'{settings.MEDIA_ROOT}/tmp/{ref}.svg', scale=1.5)
            my_canvas = canvas.Canvas(f'{settings.MEDIA_ROOT}/tmp/{ref}.pdf',
                                      pagesize=letter)
            drawing = svg2rlg(f'{settings.MEDIA_ROOT}/tmp/{ref}.svg')
            renderPDF.draw(drawing, my_canvas, self.pdf_tools.pos_x,
                           self.pdf_tools.pos_y)
            self.pdf_tools.add_text(my_canvas, 'Verifique el documento en',
                                    self.pdf_tools.pos_y - 8)
            self.pdf_tools.add_text(my_canvas, WEB_CLIENT_URL, self.pdf_tools.pos_y - 16)
            my_canvas.save()
            return sha_256.hexdigest(), md_5
        except Exception as e:
            print(e)
            print('__createQR')
            return None

    def create_hash_256_qr(self, file=None):
        try:
            file = base64.b64encode(file)
            sha_256 = self.__encrypt_document_sha256(file_base64=file)
            return sha_256.hexdigest()
        except Exception as e:
            print(e)
            print('create_hash_256_qr')
            return None