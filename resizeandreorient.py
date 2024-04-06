from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation
from PyPDF2.generic import RectangleObject

def to_specific_size_and_orientation(input_filename, target_size, target_orientation):
    output_file = f"converted_{input_filename}"
    reader = PdfReader(input_filename)
    writer = PdfWriter()
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        target_width, target_height = get_page_dimensions(target_size, target_orientation)
        height = float(page.mediabox.height)
        width = float(page.mediabox.width)
        scale_by = min(target_height/height, target_width/width)
        transform = Transformation().scale(sx=scale_by, sy=scale_by)

        if target_orientation.lower() == "landscape":
            rotation_transform = Transformation().rotate(90)
            page.add_transformation(rotation_transform)

        page.add_transformation(transform)
        page.cropbox = RectangleObject((0, 0, target_width, target_height))
        A5page = PageObject.create_blank_page(width=target_width, height=target_height)
        page.mediabox = A5page.mediabox
        A5page.merge_page(page)
        writer.add_page(A5page)

    writer.write(output_file)
    writer.close()

def get_page_dimensions(page_size, orientation): 
    sizes = { 'a0': (2384, 3370), 
             'a1': (1684, 2384), 
             'a2': (1190, 1684), 
             'a3': (841, 1190), 
             'a4': (595, 841), 
             'a5': (419, 595), 
             'letter': (612, 792), 
             'legal': (612, 1008), } 
    width, height = sizes[page_size.lower()] 
    if orientation.lower() == 'landscape': 
        return height, width 
    return width, height 
def main(): 
    input_files = [] 
    num_pdfs = int(input("Enter the number of PDF files: ")) 
    for _ in range(num_pdfs): pdf_file = input(f"Enter the filename for PDF {_ + 1}: ") 
    input_files.append(pdf_file) 
    target_size = input("Enter target page size (e.g., A5, A4, etc.): ") 
    target_orientation = input("Enter target orientation (portrait or landscape): ") 
    for input_file in input_files: 
        to_specific_size_and_orientation(input_file, target_size, target_orientation) 
if __name__ == "__main__": 
    main()
