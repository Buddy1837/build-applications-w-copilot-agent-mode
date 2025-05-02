import pytesseract
from PIL import Image
from PIL import ImageFilter, ImageOps

# Set path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Load an image and run OCR
img = Image.open('guj.png')
text = pytesseract.image_to_string(img, lang='guj')
print(text)
# Preprocess the image to improve OCR accuracy

# Convert image to grayscale
img = img.convert('L')

# Apply thresholding to binarize the image
img = img.point(lambda x: 0 if x < 128 else 255, '1')

# Apply filters to reduce noise
img = img.filter(ImageFilter.MedianFilter(size=3))

# Optionally invert the image if needed
img = ImageOps.invert(img)

# Save the preprocessed image for debugging
img.save('preprocessed_guj.png')

# Run OCR on the preprocessed image
text = pytesseract.image_to_string(img, lang='guj')
print(text)

