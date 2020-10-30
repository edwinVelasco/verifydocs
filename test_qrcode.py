import pyqrcode
import datetime
import PyPDF2
import hashlib
import base64

from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def createQR():
    data = dict(token='b8f40e61aaf47a85eeba8ee3886294e7',
                url='https://verifydocs.ufps.edu.co/verify/5/')
    data2 = f"token={data['token']}\n{data['url']}"
    WEB_CLIENT_URL = 'https://verifydocs.ufps.edu.co/'
    # xy = [170, 38, 480, 10]
    # xy = [160, 80, 500, 60]
    xy = [160, 80, 200, 250]
    date = datetime.datetime.now()
    type_doc = 'CN'
    code = '18282004'
    ref = f"{date.strftime('%Y%m%d%H%M%S')}COD{code}" \
          f"{type_doc}"

    url = f'{WEB_CLIENT_URL}{ref}'
    print(len(str(data)))
    qr2 = pyqrcode.create(str(data))
    qr2.svg(f'temp/{ref}.svg', scale=3)

    my_canvas = canvas.Canvas(f'temp/{ref}.pdf', pagesize=letter)
    drawing = svg2rlg(f'temp/{ref}.svg')
    renderPDF.draw(drawing, my_canvas, xy[2], xy[3])
    my_canvas.setFont("Times-Roman", 10)
    my_canvas.drawString(xy[0], xy[1],
                         'Verifique la autenticidad de este documento en')
    my_canvas.drawString(xy[0]-65, xy[1]-10,
                         f'{WEB_CLIENT_URL} con el código {ref}')
    my_canvas.save()
    return ref


def create_pdf_out(ref):
    file = open('pol.pdf', 'rb')
    reader = PyPDF2.PdfFileReader(file)
    page = reader.getPage(0)

    water = open(f'temp/{ref}.pdf', 'rb')
    reader2 = PyPDF2.PdfFileReader(water)
    waterpage = reader2.getPage(0)
    page.mergePage(waterpage)
    writer = PyPDF2.PdfFileWriter()
    writer.addPage(page)
    for pageNum in range(1,
                         reader.numPages):  # this will give length of book
        pageObj = reader.getPage(pageNum)
        writer.addPage(pageObj)
    resultFile = open(f'temp/{ref}_origin.pdf', 'wb')  # here we are
    # writing so
    # 'wb' is for write binary

    writer.write(resultFile)
    file.close()
    resultFile.close()


def sha_256_def(ref):
    file = open(f'temp/{ref}.pdf', 'rb').read()
    encoded = base64.b64encode(file)
    print(encoded, '')
    sha_256 = hashlib.sha256(encoded)
    print(sha_256.hexdigest())
    #print(sha_256.digest())
    # sha512
    sha_512 = hashlib.sha512(sha_256.digest())
    # print(md_5.digest())
    print(sha_512.hexdigest())

    md_5 = hashlib.md5(sha_512.digest())
    #print(md_5.digest())
    print(md_5.hexdigest())


#ref = createQR()
#sha_256_def(ref=ref)
# create_pdf_out(ref)
