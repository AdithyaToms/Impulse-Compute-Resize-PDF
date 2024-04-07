import PyPDF2
from PyPDF2.generic import RectangleObject

def to_specific_size_and_orientation(input_file, output_file, target_size, target_orientation):
    with open(input_file, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            if(target_orientation=="landscape"):
                page.rotate(-90)
            target_width, target_height = get_page_dimensions(target_size)
            height = float(page.mediabox.height)
            width = float(page.mediabox.width)
            scale_by = min(target_height/height,target_width/width)
            transform = PyPDF2.Transformation().scale(sx=scale_by,sy=scale_by).translate(tx=(target_width-width*scale_by)/2, ty=(target_height-height*scale_by)/2)
            page.add_transformation(transform)
            page.cropbox = RectangleObject((0, 0, target_width, target_height))
            writer = PyPDF2.PdfWriter()
            writer.add_page(page)
            writer.write(output_file)
            writer.close()

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
