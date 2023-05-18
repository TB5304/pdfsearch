import streamlit as st
import fitz
import pytesseract
from collections import Counter

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def perform_ocr_on_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_text = ""
    for page in doc:
        image_list = page.get_images()
        for image in image_list:
            xref = image[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            image_path = f"temp_image.png"
            with open(image_path, "wb") as f:
                f.write(image_data)
            text = pytesseract.image_to_string(image_path)
            extracted_text += text
    return extracted_text

def tokenize(extracted_text):
    x=extracted_text.replace('\n',' ').replace('/',' ').split(" ")
    v=[]
    for i in x:
        if len(i)==1:
            if i not in ['',',','?','-','&',':', ':', ':', ':', 'T', 'D', 'C', ':', '|', '|', ':', '\\', '—', ':', '/', ':', ':',':¢', '-—']:
                v.append(i)
        else:
            xmx=i
            xmx=xmx.replace('?','')
            xmx=xmx.replace('.','')
            xmx=xmx.replace(',','')
    #         xmx=xmx.replace('/','')
            xmx=xmx.replace('(','')
            xmx=xmx.replace(')','')
            if xmx !='':
                v.append(xmx)
    return v
def highlight_text(text, search_terms):
    highlighted_text = text
    for term in search_terms:
        highlighted_text = highlighted_text.replace(term, f"<mark>{term}</mark>")
    return highlighted_text

def main():
    st.title("PDF Text Extraction and Search")

    # File upload
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        pdf_path = "temp.pdf"  # Save the uploaded file temporarily
        with open(pdf_path, "wb") as f:
            f.write(file_contents)

        # OCR option
        perform_ocr = st.checkbox("Perform OCR")

        if not perform_ocr:
            extracted_text = extract_text_from_pdf(pdf_path)
        else:
            extracted_text = perform_ocr_on_pdf(pdf_path)

        # Tokenize extracted text
        tokens = tokenize(extracted_text)

        # Search input
        search_input = st.text_input("Enter strings to search (separated by commas)")
        highlighted_text = extracted_text
        ###############################
        
        if search_input:
            search_terms = [term.strip() for term in search_input.split(",")]
            search_results = [token for token in tokens if any(term.lower() in token.lower() for term in search_terms)]
#             #####################################
            
            highlighted_text = extracted_text

            # Highlight search results in extracted text
            if search_results:
                highlighted_text = highlight_text(extracted_text, search_results)
            
            
            word_count = Counter(tokens)
            search_results = {term: word_count.get(term, 0) for term in search_terms}

            # Display search term counts
            st.subheader("Search Results")
            for term, count in search_results.items():
                st.write(f"{term}: {count}")
            
            
#             # Display search results
#             st.subheader("Search Results")
#             if search_results:
#                 st.write(search_results)
#             else:
#                 st.info("No matching results found.")

        # Display extracted text with highlighting
        st.subheader("Extracted Text")
        st.markdown(highlighted_text, unsafe_allow_html=True)
            
            
            ##########################################
            
            
            
            
            
#             # Display search results
#             st.subheader("Search Results")
#             if search_results:
#                 st.write(search_results)
#             else:
#                 st.info("No matching results found.")

#         # Display extracted text
#         st.subheader("Extracted Text")
#         st.text_area("Extracted Text", value=extracted_text, height=300)

    else:
        st.warning("Please upload a PDF file.")

if __name__ == "__main__":
    main()
