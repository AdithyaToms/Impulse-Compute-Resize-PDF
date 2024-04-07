from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

def to_specific_size_and_orientation(input_file, output_file, target_size,target_orientation):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    target_width, target_height = get_page_dimensions(target_size)
    r = RectangleObject([0, 0, target_width, target_height])

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if(target_orientation=="landscape" and width<height):
            page.rotate(-90)
        elif(target_orientation=="portrait" and width>height):
            page.rotate(90)
        scale_by = min(target_height/height, target_width/width)

        new_width = float(width * scale_by)
        new_height = float(height * scale_by)

        dx = (target_width - new_width) / 2
        dy = (target_height - new_height) / 2
        transform = Transformation().translate(tx=dx, ty=dy)

        page.scale_to(width=new_width, height=new_height)
        page.add_transformation(transform)
        page.mediabox = r
        page.artbox = r
        page.cropbox = r
        page.bleedbox = r
        page.trimbox = r
        writer.add_page(page)

    with open(output_file, "wb"):
        writer.write(output_file)

def get_page_dimensions(page_size): 
    sizes = { 'a0': (2384, 3370), 
             'a1': (1684, 2384), 
             'a2': (1191, 1684), 
             'a3': (842, 1191), 
             'a4': (595, 842), 
             'a5': (420, 595), 
             'letter': (612, 791), 
             'legal': (612, 1009), 
             'tabloid': (1225, 791), 
             'ledger': (791,1225), 
             'executive': (522,756), 
             } 
    width, height = sizes[page_size.lower()] 
    return width, height 
def main(): 
    input_files = [] 
    num_pdfs = int(input("Enter the number of PDF files: ")) 
    for _ in range(num_pdfs): 
        pdf_file = input(f"Enter the filename for PDF {_ + 1}: ") 
        input_files.append(pdf_file) 
    target_size = input("Enter target page size (e.g., A5, A4, etc.): ") 
    target_orientation = input("Enter target orientation (portrait or landscape): ") 
    for input_file in input_files: 
        output_file = f"converted_{input_file}"
        to_specific_size_and_orientation(input_file, output_file, target_size, target_orientation) 

if __name__ == "__main__": 
    main()
