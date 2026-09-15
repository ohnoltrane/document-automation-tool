import os
from PyPDF2 import PdfReader, PdfWriter

# Run Script: python <script_path>

folder = r"<folder_path>"  # Change to your folder containing LoAs(a.k.a. first page of desired doc)
append_pdf_folder = r"<folder_path>" # Change to folder containing appendix PDFs
output_folder = r"<output_folder_path>" # Change to folder you want to output to

def find_appendix_pdf(schedule_number):
    for f in os.listdir(append_pdf_folder):
        if f.lower().endswith('.pdf') and f"schedule {schedule_number}" in f.lower():
            return os.path.join(append_pdf_folder, f)
    return None

appendix_pdf_1 = find_appendix_pdf(1) # Make sure PDF has "Schedule 1" in its filename
appendix_pdf_2 = find_appendix_pdf(2) # Make sure PDF has "Schedule 2" in its filename
appendix_pdf_3 = find_appendix_pdf(3) # Make sure PDF has "Schedule 3" in its filename

appendix_pdfs = [appendix_pdf_1, appendix_pdf_2, appendix_pdf_3]

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf") and filename != os.path.basename(append_pdf_folder):
        pdf_path = os.path.join(folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_full.pdf")

        writer = PdfWriter()

        # Add original PDF pages
        with open(pdf_path, "rb") as orig_file:
            reader = PdfReader(orig_file)
            for page in reader.pages:
                writer.add_page(page)

        # Add appendix pages (open file each time)
        for appendix_pdf in appendix_pdfs:
            if appendix_pdf:
                with open(appendix_pdf, "rb") as f:
                    appendix_reader = PdfReader(f)
                    for page in appendix_reader.pages:
                        writer.add_page(page)

        # Write the new PDF
        with open(output_path, "wb") as out_file:
            writer.write(out_file)

        print(f"Appended appendix PDFs to {pdf_path} -> {output_path}")
