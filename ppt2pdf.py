import os
from typing import List

import win32com.client
from PyPDF2 import PdfFileReader, PdfFileWriter


def split_pdf(pdf_file_path: str):
    """Split a sinlge PDF file with every page a new PDF file.
    """
    ...

def ppt2pdf(root_dir: str, ppt_file_name: str, result_file_names: List[str]):
    """Convert PPT into a single PDF
    """
    # open PPT
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")
    # powerpoint.Visible = True

    # convert
    ppt_file_path = os.path.join(root_dir, ppt_file_name)
    deck = powerpoint.Presentations.Open(ppt_file_path) 
    tmp_result_file_path = os.path.join(root_dir, "tmp.pdf")      
    deck.SaveAs(tmp_result_file_path, 32)
    powerpoint.Quit()
    deck.Close()

    # split
    pdf_reader = PdfFileReader(tmp_result_file_path)
    page_num = pdf_reader.getNumPages()
    assert page_num == len(result_file_names)

    for i in range(page_num):
        output = PdfFileWriter()
        output.addPage(pdf_reader.getPage(i))
        output_file_path = os.path.join(root_dir, result_file_names[i] + ".pdf")
        with open(output_file_path, "ab") as output_pdf:
            output.write(output_pdf)

    # clean
    os.remove(tmp_result_file_path)


if __name__ == "__main__":
    root_dir = "I:\\result"
    ppt_file_name = "envs.pptx"
    result_file_names = ["line1", "line2", "line3", "line4"]
    ppt2pdf(root_dir, ppt_file_name, result_file_names)