from PyPDF2 import PdfWriter, PdfReader


from PyPDF2.generic import BooleanObject, NameObject, IndirectObject



reader = PdfReader("forms/LIC9052.pdf")
writer = PdfWriter()

page = reader.pages[0]
fields = reader.get_fields()
print(f"Fields for LIC 9052 : {fields}")

fields2 = reader.get_form_text_fields()
print(f"form => {fields2}")


data = {
    'LIC 9052 1': {'/T': 'LIC 9052 1', '/FT': '/Tx', '/TU': 'NAME OF EMPLOYEE', '/V': "Justin Fields"},
    'LIC 9052 5': {'/T': 'LIC 9052 5', '/FT': '/Tx', '/TU': 'DATE OF SIGNATURE', '/AA': {}, '/V': "01/21/2023"},
    'LIC 9052 2': {'/T': 'LIC 9052 2', '/FT': '/Tx', '/TU': 'NAME OF EMPLOYER', '/AA': {}, '/V': "Mike Dikta"},
    'LIC 9052 3': {'/T': 'LIC 9052 3', '/FT': '/Tx', '/TU': 'NAME OF FACILITY', '/AA': {}, '/V': "Chicago Bears"},

}

data2 = {
    'LIC 9052 1': 'Justin Fields',
    'LIC 9052 5': '01/21/2023',
    'LIC 9052 2': 'Mike Dikta',
    'LIC 9052 3': 'Chicago Bears',
}


writer.add_page(page)
writer.update_page_form_field_values(
    writer.pages[0], fields=data2
)

#write "output" to PyPDF2-output.pdf
with open("output/LIC9052_filled.pdf", "wb") as output_stream:
    writer.write(output_stream)