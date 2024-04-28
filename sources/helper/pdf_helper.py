# import fitz

# pdf = r'D:\temp\target.pdf'
# doc = fitz.open(pdf)
# out = open(r"d:\temp\output.txt", "wb") 
# for page in doc: # iterate the document pages
# 	text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
# 	out.write(text) # write text of page
# 	out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
# out.close()
# print("done")


import pdfplumber

pdf = pdfplumber.open(r'D:\temp\target.pdf')
pages = pdf.pages
text = pages[0].extract_text()
print("done")
