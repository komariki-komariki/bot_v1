from docxtpl import DocxTemplate
from datetime import datetime


def word_employer (my_dict):
    doc = DocxTemplate("kontr.docx")
    context = my_dict
    doc.render (context)
    short_name = my_dict["abr_name"].replace('"', "")
    date = datetime.datetime.now().date().strftime('%d.%m.%Y')
    file_name = f"{short_name}_{date}.docx"
    doc.save(file_name)
    return file_name