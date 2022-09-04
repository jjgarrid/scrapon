# Create a LateX document using PyLatex
# and convert it to PDF using pdflatex

from pylatex import Document, Section, Subsection, Command, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number, NewPage
from pylatex.utils import italic, bold, NoEscape


def generate_header(doc):
   
    # Add document header
    header = PageStyle("header")
    # Create left header
    with header.create(Head("L")):
        header.append("Page date: ")
        header.append(LineBreak())
        header.append(NoEscape(r'\today'))
    # Create center header
    with header.create(Head("C")):
        header.append("Generado por [TBD]")
    # Create right header
    with header.create(Head("R")):
        header.append(simple_page_number())
    # Create left footer
    # with header.create(Foot("L")):
    #     header.append("Left Footer")
    # Create center footer
    with header.create(Foot("C")):
        header.append("Generado automaticamente")
    # Create right footer
    # with header.create(Foot("R")):
    #     header.append("Right Footer")

    doc.preamble.append(header)
    doc.change_document_style("header")

    # Add Heading
    # with doc.create(MiniPage(align='c')):
    #     doc.append(LargeText(bold("Title")))
    #     doc.append(LineBreak())
    #     doc.append(MediumText(bold("As at:")))

    


def fill_document(doc):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')


if __name__ == '__main__':
    # Basic document
    geometry_options = {"margin": "0.7in"}
    doc = Document('basic', geometry_options=geometry_options)

    doc.preamble.append(Command('title', 'Información Local'))
    doc.preamble.append(Command('author', 'Generado por [TBD]'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    doc.append(NewPage())
    generate_header(doc)
    doc.append(NoEscape(r'\tableofcontents'))
    doc.append(NewPage())
    generate_header(doc)

    fill_document(doc)

    # Add stuff to the document
    with doc.create(Section('A second section')):
        doc.append('Some text.')

    doc.generate_pdf('gen_document', clean_tex=False)
    tex = doc.dumps()  # The document as string in LaTeX syntax