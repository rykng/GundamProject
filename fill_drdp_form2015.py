from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.filters import FlateDecode

from PyPDF2.constants import (
    FieldFlag,
    PageAttributes,
    AnnotationDictionaryAttributes, InteractiveFormDictEntries,
    StreamAttributes,
    FilterTypes,
    FieldDictionaryAttributes,
)

from PyPDF2.generic import (
    BooleanObject, NameObject,
    IndirectObject,
    TextStringObject,
    NumberObject,
    encode_pdfdocencoding,
)


filename = "forms/DRDP2015_P16.pdf"
output = "output/DRDP2015_P16_filled.pdf"


# Example data.
data2 = {
    'Other programs that child is enrolled in 1': None,
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
    "Early Education Info Page: Child's last name 1": "Ng\n",
    "Early Education Info Page: Child's first name 1": "Kaylee\n"},


# Get template.
template = PdfReader(filename, strict=False)

# Initialize writer.
writer = PdfWriter()

# Add the template page.
writer.add_page(template.pages[0])

# Get page annotations.
page_annotations = writer.pages[0][PageAttributes.ANNOTS]

# Loop through page annotations (fields).
for index in range(len(page_annotations)):  # type: ignore
    # Get annotation object.
    annotation = page_annotations[index].get_object()  # type: ignore

    # Get existing values needed to create the new stream and update the field.
    field = annotation.get(NameObject("/T"))
    new_value = data2.get(field, 'N/A')
    ap = annotation.get(AnnotationDictionaryAttributes.AP)
    x_object = ap.get(NameObject("/N")).get_object()
    font = annotation.get(InteractiveFormDictEntries.DA)
    rect = annotation.get(AnnotationDictionaryAttributes.Rect)

    # Calculate the text position.
    font_size = float(font.split(" ")[1])
    w = round(float(rect[2] - rect[0] - 2), 2)
    h = round(float(rect[3] - rect[1] - 2), 2)
    text_position_h = h / 2 - font_size / 3  # approximation

    # Create a new XObject stream.
    new_stream = f'''
        /Tx BMC 
        q
        1 1 {w} {h} re W n
        BT
        {font}
        2 {text_position_h} Td
        ({new_value}) Tj
        ET
        Q
        EMC
    '''

    # Add Filter type to XObject.
    x_object.update(
        {
            NameObject(StreamAttributes.FILTER): NameObject(FilterTypes.FLATE_DECODE)
        }
    )

    # Update and encode XObject stream.
    x_object._data = FlateDecode.encode(encode_pdfdocencoding(new_stream))

    # Update annotation dictionary.
    annotation.update(
        {
            # Update Value.
            NameObject(FieldDictionaryAttributes.V): TextStringObject(
                new_value
            ),
            # Update Default Value.
            NameObject(FieldDictionaryAttributes.DV): TextStringObject(
                new_value
            ),
            # Set Read Only flag.
            NameObject(FieldDictionaryAttributes.Ff): NumberObject(
                FieldFlag(1)
            )
        }
    )

# Clone document root & metadata from template.
# This is required so that the document doesn't try to save before closing.
writer.clone_reader_document_root(template)

# write "output".
with open(output, "wb") as output_stream:
    writer.write(output_stream)  # type: ignore
