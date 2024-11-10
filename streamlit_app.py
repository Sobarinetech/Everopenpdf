import streamlit as st
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
import pdf2docx
import docx2pdf
import os

# PDF Merger
def merge_pdfs(pdf_files):
    merger = PyPDF2.PdfMerger()
    for file in pdf_files:
        try:
            with open("temp.pdf", "wb") as f:
                f.write(file.getbuffer())
            merger.append("temp.pdf")
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
    merged_pdf = merger.write("merged.pdf")
    os.remove("temp.pdf")
    return merged_pdf

# PDF Splitter
def split_pdf(pdf_file, page_range):
    try:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.getbuffer())
        pdf = PyPDF2.PdfReader("temp.pdf")
        writer = PyPDF2.PdfWriter()
        for page_num in range(page_range[0], page_range[1]+1):
            writer.add_page(pdf.pages[page_num-1])
        output_pdf = writer.write("split.pdf")
        os.remove("temp.pdf")
        return output_pdf
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")

# PDF Compressor
def compress_pdf(pdf_file):
    try:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.getbuffer())
        pdf = PyPDF2.PdfReader("temp.pdf")
        writer = PyPDF2.PdfWriter()
        for page in pdf.pages:
            writer.add_page(page)
        compressed_pdf = writer.write("compressed.pdf")
        os.remove("temp.pdf")
        return compressed_pdf
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")

# PDF to Word Converter
def pdf_to_word(pdf_file):
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.getbuffer())
    converter = pdf2docx.Converter("temp.pdf")
    docx_file = converter.convert()
    os.remove("temp.pdf")
    return docx_file

# PDF to JPG Converter
def pdf_to_jpg(pdf_file):
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.getbuffer())
    images = convert_from_path("temp.pdf")
    jpg_files = []
    for i, image in enumerate(images):
        jpg_file = f"page_{i+1}.jpg"
        image.save(jpg_file, "JPEG")
        jpg_files.append(jpg_file)
    os.remove("temp.pdf")
    return jpg_files

# Streamlit App
st.title("PDF Tools")

# PDF Merger
st.header("PDF Merger")
pdf_files = st.file_uploader("Select PDF files to merge", type=["pdf"], accept_multiple_files=True, key="merge_uploader")
if st.button("Merge PDFs"):
    merged_pdf = merge_pdfs(pdf_files)
    st.download_button("Download Merged PDF", "merged.pdf", file_name="merged.pdf")

# PDF Splitter
st.header("PDF Splitter")
pdf_file = st.file_uploader("Select PDF file to split", type=["pdf"], key="split_uploader")
page_range = st.slider("Select page range", 1, 100, (1, 10), key="split_slider")
if st.button("Split PDF"):
    split_pdf = split_pdf(pdf_file, page_range)
    st.download_button("Download Split PDF", "split.pdf", file_name="split.pdf")

# PDF Compressor
st.header("PDF Compressor")
pdf_file = st.file_uploader("Select PDF file to compress", type=["pdf"], key="compress_uploader")
if st.button("Compress PDF"):
    compressed_pdf = compress_pdf(pdf_file)
    st.download_button("Download Compressed PDF", "compressed.pdf", file_name="compressed.pdf")

# PDF to Word Converter
st.header("PDF to Word Converter")
pdf_file = st.file_uploader("Select PDF file to convert", type=["pdf"], key="word_uploader")
if st.button("Convert to Word"):
    docx_file = pdf_to_word(pdf_file)
    st.download_button("Download Word Document", docx_file, file_name="document.docx")

# PDF to JPG Converter
st.header("PDF to JPG Converter")
pdf_file = st.file_uploader("Select PDF file to convert", type=["pdf"], key="jpg_uploader")
if st.button("Convert to JPG"):
    jpg_files = pdf_to_jpg(pdf_file)
    for jpg_file in jpg_files:
        st.image(jpg_file)
        os.remove(jpg_file)
