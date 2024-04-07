from pypdf import PdfReader, PdfWriter
def to_specific_size_and_orientation(input_file, output_file, target_size, target_orientation):
    target_orientation=target_orientation.lower()
    with open(input_file, 'rb') as file:
        pdf = PdfReader(file)
        writer = PdfWriter()
        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            height = float(page.mediabox.height)
            width = float(page.mediabox.width)
            if(target_orientation=="landscape" and width<height):
                page.rotate(-90)
            elif(target_orientation=="portrait" and width>height):
                page.rotate(90)
            target_width, target_height = get_page_dimensions(target_size)
            page.scale_to(width=target_width, height=target_height)
            page.artbox = page.mediabox
            page.cropbox = page.mediabox
            page.bleedbox = page.mediabox
            page.trimbox =  page.mediabox
            page.transfer_rotation_to_content()
            writer.add_page(page)
        with open(output_file, 'wb') as out_file:
            writer.write(out_file)

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
    for i in range(num_pdfs): 
        pdf_file = input(f"Enter the filename for PDF {i + 1}: ") 
        input_files.append(pdf_file) 
    target_size = input("Enter target page size (e.g., A5, A4, etc.): ") 
    target_orientation = input("Enter target orientation (portrait or landscape): ") 
    for input_file in input_files: 
        output_file = f"converted_{input_file}"
        to_specific_size_and_orientation(input_file, output_file, target_size, target_orientation) 

if __name__ == "__main__": 
    main()
