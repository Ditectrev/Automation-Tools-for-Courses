import PyPDF2 as p2
import xlsxwriter

pdfFileName = "sample.pdf"
pdfFile = open(pdfFileName, 'rb')
pdfread = p2.PdfFileReader(pdfFile)
number_of_pages = pdfread.getNumPages()
workbook = xlsxwriter.Workbook('pdftoexcel.xlsx')

for page_number in range(number_of_pages):
    print(f'Sheet{page_number}')
    pageinfo = pdfread.getPage(page_number)
    rawInfo = pageinfo.extractText().split('\n')

    row = 0
    column = 0
    worksheet = workbook.add_worksheet(f'Sheet{page_number}')

    for line in rawInfo:
        worksheet.write(row, column, line)
        row += 1
workbook.close()