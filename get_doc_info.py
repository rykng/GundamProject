from PyPDF2 import PdfReader, PdfWriter


def get_info(path):
    with open(path, 'rb') as f:
        reader = PdfReader(f)
        md = reader.metadata
        num_of_pages = len(reader.pages)

    print(md)
    print(f"author => {md.author}")
    print(f"creator => {md.creator}")
    print(f"producer => {md.producer}")
    print(f"subject => {md.subject}")
    print(f"title => {md.title}")
    print(f"num of pages => {num_of_pages}")



def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfReader(f)
        # get the first page
        page = pdf.pages[0]
        print(page)
        print('Page type: {}'.format(str(type(page))))
        text = page.extract_text()
        print(text)




def get_page_object(path):
    with open(path, 'rb') as f:
        pdf = PdfReader(f)
        # get the first page
        page = pdf.pages[0]
        return page


def write_data_to_output(reader_path, output, data):
    reader = PdfReader(reader_path)
    writer = PdfWriter()

    page = reader.pages[0]
    fields = reader.get_form_text_fields()
    print(f"form fields => {fields}")

    writer.add_page(page)
    writer.update_page_form_field_values(
        writer.pages[0], data
    )

    # write "output" to PyPDF2-output.pdf
    with open(output, "wb") as output_stream:
        writer.write(output_stream)
        print(f"finish writing data to {output}")


if __name__ == '__main__':
    path = 'forms/fw9.pdf'
    output = 'output/fw9_filled.pdf'

    data_fw9 = {'f1_1[0]': "Aaron Rodgers", 'f1_2[0]': "Green Bay Packers", 'f1_3[0]': "P" }

    get_info(path)
    write_data_to_output(path, output,data_fw9)

