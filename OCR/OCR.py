import pytesseract
from PIL import Image

# Set path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load an image and run OCR
img = Image.open('guj.png')
text = pytesseract.image_to_string(img, lang='guj')
print(text)
