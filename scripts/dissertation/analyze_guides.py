import fitz  # PyMuPDF
import docx
import os

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF {pdf_path}: {e}"

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX {docx_path}: {e}"

def analyze_guides(guides_dir):
    files = [
        "Dissertation Format Guide.pdf",
        "Dissertation Headings.pdf",
        "Referencing Guide.pdf",
        "Sample Dissertation. Postgraduate. Richfield.pdf", 
        "Dissertation Support Session - 03112025-en-US.docx"
    ]
    
    analysis_report = ""
    
    for filename in files:
        file_path = os.path.join(guides_dir, filename)
        analysis_report += f"\n\n--- ANALYSIS OF: {filename} ---"
        
        if filename.endswith(".pdf"):
            content = extract_text_from_pdf(file_path)
        elif filename.endswith(".docx"):
            content = extract_text_from_docx(file_path)
        else:
            content = "Unsupported file type."

        # Limit output for the report to avoid token limits, but capture enough key info
        # specifically looking for keywords like "Heading", "Font", "Margin", "Reference"
        lines = content.split('\n')
        
        # Simple keyword extraction for the report
        relevant_lines = []
        capture = False
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Heuristic: Capture headings or lines with key formatting terms
            lower_line = line.lower()
            if any(k in lower_line for k in ["heading", "font", "margin", "spacing", "reference", "citation", "table of contents", "structure", "chapter"]):
                relevant_lines.append(line)
            # Capture first 20 lines of sample dissertation to see structure
            if "sample dissertation" in filename.lower() and len(relevant_lines) < 50:
                relevant_lines.append(line)

        # Join a subset of relevant lines
        analysis_report += "\n".join(relevant_lines[:100]) # limit to 100 relevant lines per file for the summary

    return analysis_report

if __name__ == "__main__":
    guides_directory = r"C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Completed\Guides"
    report = analyze_guides(guides_directory)
    
    # Write report to file so we can read it via cat
    with open("guides_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("Analysis complete. Report saved to guides_analysis_report.txt")
