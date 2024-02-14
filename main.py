import io
import os
import fitz  # PyMuPDF
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np

def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append((Image.open(io.BytesIO(image_bytes)), xref))
    return images

def compare_images(imageA, imageB):
    # Convertir les images en niveaux de gris
    imageA = imageA.convert('L')
    imageB = imageB.convert('L')
    imageA = np.array(imageA)
    imageB = np.array(imageB)
    # Calculer SSIM entre deux images
    score, _ = ssim(imageA, imageB, full=True)
    return score

def find_most_frequent_image(images):
    max_count = 0
    most_frequent_image = None
    most_frequent_xref = None
    for i, (img1, xref1) in enumerate(images):
        count = 1
        for j, (img2, xref2) in enumerate(images):
            if i != j and compare_images(img1, img2) > 0.95:  # Seuil de similarité
                count += 1
        if count > max_count:
            max_count = count
            most_frequent_image = img1
            most_frequent_xref = xref1
    return most_frequent_image, most_frequent_xref, max_count

def remove_most_frequent_image(pdf_path, xref):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for img in page.get_images(full=True):
            if img[0] == xref:
                page.delete_image(xref)
    return doc

# Chemin vers votre fichier PDF
pdf_path = 'fichier.pdf'
images = extract_images_from_pdf(pdf_path)
most_frequent_image, most_frequent_xref, count = find_most_frequent_image(images)

# Enregistrer l'image la plus fréquente
if most_frequent_image:
    most_frequent_image.save('image_la_plus_frequente.png')
    print(f"L'image la plus fréquente a été trouvée {count} fois et a été enregistrée.")
    # Supprimer l'image la plus fréquente du PDF et enregistrer le fichier modifié
    modified_doc = remove_most_frequent_image(pdf_path, most_frequent_xref)
    # Construire le nouveau nom de fichier
    base_name, ext = os.path.splitext(pdf_path)
    modified_pdf_path = f"{base_name}_modified{ext}"
    modified_doc.save(modified_pdf_path)
    print(f"L'image la plus fréquente a été supprimée du fichier PDF. Le fichier modifié est enregistré sous {modified_pdf_path}.")
else:
    print("Aucune image fréquente trouvée.")
