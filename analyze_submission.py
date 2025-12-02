import fitz  # PyMuPDF
import re

def analyze_pdf(pdf_path, check_turnitin=False):
    print(f"\n--- Analyzing: {pdf_path} ---")
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        # Read first 10 pages for Front Matter & Chapter 1
        for i in range(min(10, len(doc))):
            page_text = doc[i].get_text()
            text += f"\n[PAGE {i+1}]\n{page_text}"
            
        # Read random middle pages for spelling check
        middle_text = ""
        if len(doc) > 50:
            for i in range(40, 45):
                middle_text += doc[i].get_text()
        
        # 1. Check Structure
        print(f"Total Pages: {len(doc)}")
        
        if "RESEARCH PROBLEM" in text or "Research Problem" in text:
            print("✅ Chapter 3 'Research Problem' detected in TOC/Body.")
        else:
            print("⚠️ Chapter 3 'Research Problem' NOT immediately detected in first 10 pages.")

        if "DISCUSSION, CONCLUSION AND RECOMMENDATIONS" in text or "Discussion, Conclusion and Recommendations" in text:
             print("✅ Chapter 6 'Discussion, Conclusion...' detected in TOC.")
        
        # 2. Check Spelling (SA vs US)
        us_terms = ["Behavior", "Labor", "Center", "Program", "Analyze"]
        sa_terms = ["Behaviour", "Labour", "Centre", "Programme", "Analyse"]
        
        print("\n--- Spelling Check (Sample) ---")
        combined_text = text + middle_text
        for us, sa in zip(us_terms, sa_terms):
            us_count = len(re.findall(r'\b' + us + r'\b', combined_text))
            sa_count = len(re.findall(r'\b' + sa + r'\b', combined_text))
            print(f"{sa} (SA): {sa_count} vs {us} (US): {us_count}")

        # 3. Turnitin Score (if applicable)
        if check_turnitin:
            print("\n--- Turnitin Check ---")
            # Usually score is on the first page
            first_page = doc[0].get_text()
            # Look for patterns like "12%" or "Similarity Index"
            match = re.search(r'(\d+)%', first_page)
            if match:
                print(f"Possible Similarity Score: {match.group(1)}%")
            else:
                print("Could not automatically detect Turnitin score on Page 1.")

    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    submission_path = r"C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Submit\Dissertation_Craig_Vraagom_402415017.pdf"
    turnitin_path = r"C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Submit\TurnItIn_Dissertation_Craig_Vraagom_402415017.pdf"
    
    analyze_pdf(submission_path)
    analyze_pdf(turnitin_path, check_turnitin=True)
