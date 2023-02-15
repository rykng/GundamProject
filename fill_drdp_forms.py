from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.constants import FieldFlag

from PyPDF2.generic import BooleanObject, NameObject, IndirectObject

def set_need_appearances_writer(writer: PdfWriter):
    # See 12.7.2 and 7.7.2 for more information: http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    try:
        catalog = writer._root_object
        # get the AcroForm tree
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer


infile = "forms/DRDP2015_P16.pdf"
output = "output/DRDP2015_P16_filled.pdf"
reader = PdfReader(infile, strict=False)
if "/AcroForm" in reader.trailer["/Root"]: # result: following "IF code is executed
    print(f"Reader set needAppearances")
    reader.trailer["/Root"]["/AcroForm"].update(
        {NameObject("/NeedAppearances"): BooleanObject(True)})


writer = PdfWriter()
writer = set_need_appearances_writer(writer)
catalog = writer._root_object
print(f"w.catalog => {catalog}")
if "/AcroForm" in writer._root_object:
    writer._root_object["/AcroForm"].update(
        {NameObject("/NeedAppearances"): BooleanObject(True)})


page = reader.pages[0]
fields = reader.get_fields()
#print(f"Fields for LIC 9052 : {fields}")

ff2 = reader.get_form_text_fields()
print(f"get_form_text_fields() => {ff2}")



data2 =  {'Other programs that child is enrolled in 1': None,
          'Role/relation of someone who understands /uses the child’s home language assist you 1': None,
          'What language(s) do you speak with this child? 1': None,
          'Child’s home language(s) 1': None,
          'Early Education Info Page: If another adult assisted, what was their role/relation? 1': None,
          'Early Education Info Page: If you are not the primary teacher, specify your relationship to child 1': None,
          'Early Education Info Page: Observer Title 1': None,
          'Early Education Info Page: Observer Name 1': None,
          'Early Education Info Page: Observer Site 1': None,
          'Early Education Info Page: Observer Agency 1': None,
          'Early Education Info Page: Year: Date child was withdrawn from the program 1': None,
          'Early Education Info Page: Day: Date child was withdrawn from the program 1': None,
          'Early Education Info Page: Month: Date child was withdrawn from the program 1': None,
          'Early Education Info Page: Year: Initial date of enrollment in early childhood program 1': None,
          'Early Education Info Page: Day: Initial date of enrollment in early childhood program 1': None,
          'Early Education Info Page: Month: Initial date of enrollment in early childhood program 1': None,
          'Early Education Info Page: Year: Birth date 1': "2014",
          'Early Education Info Page: Day: Birth date 1': "19",
          'Early Education Info Page: Month:Birth date 1': "02",
          'Early Education Info Page: Child’s classroom or setting 1': "Classroom",
          'Early Education Info Page: Agency Identifier 1': None,
          'Early Education Info Page: Statewide Student Identifier 1': None,
          'Early Education Info Page: Assessment period': "Fall 2022",
          'Early Education Info Page: Year: Date DRDP (2015) was completed 1': "2023",
          'Early Education Info Page: Day: Date DRDP (2015) was completed 1': "10",
          'Early Education Info Page: Month: Date DRDP (2015) was completed  1': "02",
          "Early Education Info Page: Child's last name 1": "Ng",
          "Early Education Info Page: Child's first name 1": "Kaylee"}


writer.add_page(page)

writer.update_page_form_field_values(
    writer.pages[0], fields=data2
)



#write "output" to PyPDF2-output.pdf
with open(output, "wb") as output_stream:
    writer.write(output_stream)


output_stream.close()