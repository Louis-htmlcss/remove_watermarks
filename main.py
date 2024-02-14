import io
import os
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim

class PDFImageProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(self.pdf_path)

    def extract_images_from_pdf(self):
        images = []
        for page in self.doc:
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                images.append((Image.open(io.BytesIO(image_bytes)), xref))
        return images

    @staticmethod
    def compare_images(imageA, imageB):
        # Convert images to grayscale and calculate SSIM
        imageA, imageB = map(lambda x: np.array(x.convert('L')), (imageA, imageB))
        score, _ = ssim(imageA, imageB, full=True)
        return score

    def find_most_frequent_image(self, images):
        max_count, most_frequent_image, most_frequent_xref = 0, None, None
        for i, (img1, xref1) in enumerate(images):
            count = sum(self.compare_images(img1, img2) > 0.95 for j, (img2, xref2) in enumerate(images) if i != j)
            if count > max_count:
                max_count, most_frequent_image, most_frequent_xref = count, img1, xref1
        return most_frequent_image, most_frequent_xref, max_count

    def remove_most_frequent_image(self, xref):
        for page in self.doc:
            for img in page.get_images(full=True):
                if img[0] == xref:
                    page.delete_image(xref)

    def save_modified_pdf(self, modified_pdf_path):
        self.doc.save(modified_pdf_path)
        print(f"The most frequent image has been removed from the PDF file. The modified file is saved as {modified_pdf_path}.")

if __name__ == "__main__":
    pdf_path = 'file.pdf'
    processor = PDFImageProcessor(pdf_path)
    images = processor.extract_images_from_pdf()
    most_frequent_image, most_frequent_xref, count = processor.find_most_frequent_image(images)

    # Remove the most frequent image from the PDF and save the modified file
    processor.remove_most_frequent_image(most_frequent_xref)
    base_name, ext = os.path.splitext(pdf_path)
    modified_pdf_path = f"{base_name}_modified{ext}"
    processor.save_modified_pdf(modified_pdf_path)