import pyqrcode
import datetime
import PyPDF2
import hashlib
import base64

from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def hash(file_bate64=None):
    # sha512 (128 characters)
    sha_512 = hashlib.sha512(file_bate64)
    # print(sha_512.digest())
    print(sha_512.hexdigest())
    # sha256 (64 characters)
    sha_256 = hashlib.sha256(sha_512.digest())
    print(sha_256.hexdigest())
    # print(sha_256.digest())

    md_5 = hashlib.md5(sha_256.digest())
    # print(md_5.digest())
    print(md_5.hexdigest())
    return sha_256.digest()


def createQR():
    file = open('temp/1150535.pdf', 'rb').read()
    encoded = base64.b64encode(file)
    sha_256 = hash(file_bate64=encoded)
    md_5 = hashlib.md5(sha_256)
    # print(md_5.digest())
    print(md_5.hexdigest())
    data = md_5.hexdigest()
    WEB_CLIENT_URL = 'https://albertove.pythonanywhere.com/'
    xy = [80, 30, 80, 40]
    # xy = [160, 80, 500, 60]
    # xy = [160, 80, 200, 250]
    ref = '1150535_1'
    qr2 = pyqrcode.create(data)
    qr2.svg(f'temp/{ref}.svg', scale=2)

    my_canvas = canvas.Canvas(f'temp/{ref}.pdf', pagesize=letter)
    drawing = svg2rlg(f'temp/{ref}.svg')
    renderPDF.draw(drawing, my_canvas, xy[2], xy[3])
    my_canvas.setFont("Times-Roman", 10)
    my_canvas.drawString(xy[0], xy[1],
                         f'Verifiquese en {WEB_CLIENT_URL}')
    # my_canvas.drawString(xy[0]-65, xy[1]-10,
    #                      f'{WEB_CLIENT_URL} con el código {ref}')
    my_canvas.save()
    return ref


def create_pdf_out(ref):
    file = open('temp/1150535.pdf', 'rb')
    reader = PyPDF2.PdfFileReader(file)
    page = reader.getPage(0)

    water = open(f'temp/{ref}.pdf', 'rb')
    reader2 = PyPDF2.PdfFileReader(water)
    waterpage = reader2.getPage(0)
    page.mergePage(waterpage)
    writer = PyPDF2.PdfFileWriter()
    writer.addPage(page)
    for pageNum in range(1, reader.numPages):  # this will give length of book
        pageObj = reader.getPage(pageNum)
        writer.addPage(pageObj)
    resultFile = open(f'temp/{ref}_out.pdf', 'wb')  # here we are
    # writing so
    # 'wb' is for write binary

    writer.write(resultFile)
    file.close()
    resultFile.close()

    file_out = open(f'temp/{ref}_out.pdf', 'rb').read()
    encoded = base64.b64encode(file_out)
    sha_256 = hash(file_bate64=encoded)
    md_5 = hashlib.md5(sha_256)
    # print(md_5.digest())
    print(md_5.hexdigest())
    return ref


def verify_docs(ref):
    file_out = open(f'temp/{ref}_out.pdf', 'rb').read()
    encoded = base64.b64encode(file_out)
    sha_256 = hash(file_bate64=encoded)
    md_5 = hashlib.md5(sha_256)
    # print(md_5.digest())
    print(md_5.hexdigest())


ref = createQR()
ref = create_pdf_out(ref=ref)


verify_docs(ref=ref)


#sha_256_def(ref=ref)
# create_pdf_out(ref)
