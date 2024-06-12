import fitz
import pandas as pd
import re

protections_keywords = ["solutions", "defense", "guarantees", "protections", "protects", "protected", "preserve", "ensuring", "enforce", "enhanced", "safeguards", "privacy-enhancing", "privacy-preserving", "encryption", "provides privacy", "motivated by privacy concerns", "guided by privacy concerns", "prevent attacks", "ensures privacy", "committed to privacy", "respecting privacy", "dedicated to privacy", "aims to protect privacy", "securing data through", "enhancing privacy", "addresses privacy", "mitigating privacy threats", "mitigates privacy threats", "protects user", "privacy safeguards", "promotes privacy", "protect privacy"]
threats_keywords = ["hijack","challenges","issues", "problems", "threats", "vulnerability", "concerns", "breach", "loss", "attack", "leak", "violates", "risk", "misuse", "exposure", "compromise", "exploitation", "fraud", "unauthorized access", "invasion", "intrusion", "problems", "threats", "breaches", "increases privacy risks", "compromises personal information", "jeopardizes", "endangers"]

def extract_paragraphs_with_keyword(pdf_path, keyword):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    sentence_endings = re.compile(r'(?<=[.!?]) +')
    
    # Initialize a list to hold the paragraphs containing the keyword
    paragraphs_with_keyword = []

    # Initialize a list to hold the page num containing the keyword
    page_num_with_keyword = []

    # Iterate through each page in the PDF
    for page_num in range(pdf_document.page_count):
        # Extract text from the page
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        
        # Split the text into paragraphs
        paragraphs = sentence_endings.split(text)
        
        # Check each paragraph for the keyword
        for sentence_num in range(len(paragraphs)):
            paragraph = paragraphs[sentence_num].strip()
            
            if(sentence_num < 1):
                lower_bound = 0
            else:
                lower_bound = sentence_num - 1
            
            if(sentence_num > len(paragraphs) - 1):
                upper_bound = len(paragraphs)
            else:
                upper_bound = sentence_num + 1

            if keyword.lower() in paragraph.lower():
                paragraphs_with_keyword.append(".".join(paragraphs[lower_bound : upper_bound]))
                page_num_with_keyword.append(page_num + 1)

    
    # Close the PDF file
    pdf_document.close()

    result = {"page_num_with_keyword": page_num_with_keyword, "paragraphs_with_keyword": paragraphs_with_keyword}
    return result 

def extract_paragraphs_with_privacy_protections_keyword(privacy_df):
    # Initialize a list to hold the paragraphs containing the keyword
    paragraphs_with_keyword = []

    # Initialize a list to hold the page num containing the keyword
    page_num_with_keyword = []

    for i, row in privacy_df.iterrows():
        page_num = row["page_num_with_keyword"]
        para_content = row["paragraphs_with_keyword"]

        for key in protections_keywords:
            if(key in para_content):
                paragraphs_with_keyword.append(para_content.strip())
                page_num_with_keyword.append(page_num)

    result = {"page_num_with_keyword": page_num_with_keyword, "paragraphs_with_privacy_protections": paragraphs_with_keyword}
    return result 

def extract_paragraphs_with_privacy_threats_keyword(privacy_df):
    # Initialize a list to hold the paragraphs containing the keyword
    paragraphs_with_keyword = []

    # Initialize a list to hold the page num containing the keyword
    page_num_with_keyword = []

    for i, row in privacy_df.iterrows():
        page_num = row["page_num_with_keyword"]
        para_content = row["paragraphs_with_keyword"]

        for key in threats_keywords:
            if(key in para_content):
                paragraphs_with_keyword.append(para_content.strip())
                page_num_with_keyword.append(page_num)

    result = {"page_num_with_keyword": page_num_with_keyword, "paragraphs_with_privacy_threats": paragraphs_with_keyword}
    return result 


# Usage example
pdf_path = "SecurityEngineering_SecondEdition.pdf"
keyword = "privacy"
result = extract_paragraphs_with_keyword(pdf_path, keyword)
privacy_df = pd.DataFrame(result)
#drop duplicates
privacy_df = privacy_df.drop_duplicates(subset='paragraphs_with_keyword')
privacy_df.to_csv("./"+ pdf_path.split(".")[0] + "_privacy_content.csv", index = False)


privacy_protections = extract_paragraphs_with_privacy_protections_keyword(privacy_df)
privacy_protections_df = pd.DataFrame(privacy_protections)
#drop duplicates
privacy_protections_df = privacy_protections_df.drop_duplicates(subset='paragraphs_with_privacy_protections')
privacy_protections_df.to_csv("./"+ pdf_path.split(".")[0] + "_privacy_protections.csv", index = False)


privacy_threats = extract_paragraphs_with_privacy_threats_keyword(privacy_df)
privacy_threats_df = pd.DataFrame(privacy_threats)
#drop duplicates
privacy_threats_df = privacy_threats_df.drop_duplicates(subset='paragraphs_with_privacy_threats')
privacy_threats_df.to_csv("./"+ pdf_path.split(".")[0] + "_privacy_threats.csv", index = False)




