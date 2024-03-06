import fitz

pdf = r'D:\temp\target.pdf'
doc = fitz.open(pdf)

print ("number of pages: %i" % doc.pageCount)
print(doc.metadata)

page1 = doc.loadPage(0)
page1text = page1.getText("text")
print(page1text)

print('DONE')