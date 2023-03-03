import PyPDF2

key = 'DMCD-2021'
pdf_reader = PyPDF2.PdfFileReader('/home/liyc/Seafile/私人资料库/Course/DM_lim2021fall/Lecture/Lecture1.pdf')
if pdf_reader.decrypt(key): print('Right Key!')

pdf_writer = PyPDF2.PdfFileWriter()
for page in range(pdf_reader.getNumPages()):
    pdf_writer.addPage(pdf_reader.getPage(page))


with open('decrypted.pdf', 'wb') as out:
    pdf_writer.write(out)