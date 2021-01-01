import PyPDF2
import os

class Encrypt():
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def do(path, password):
        print(path, password)

        pdfFile = open(path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFile)

        pdfWriter = PyPDF2.PdfFileWriter()

        for pageNum in range(pdfReader.numPages):
            pdfWriter.addPage(pdfReader.getPage(pageNum))

        pdfWriter.encrypt(password)

        newFileName = os.path.basename(path)

        pdfFile_new = open(newFileName, 'wb')
        pdfWriter.write(pdfFile_new)

        pdfFile_new.close()
        pdfFile.close()

