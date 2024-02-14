# PDF Watermark Remover 🚫🖼️

This Python script utilizes the power of PyMuPDF and PIL libraries to identify and remove the most frequently occurring image (often a watermark) from a PDF file. It's an efficient way to clean up your PDFs from unwanted images without compromising the integrity of the document.

## Features ✨

- **Extract Images**: Scans through each page of the PDF to extract images.
- **Image Comparison**: Utilizes Structural Similarity Index (SSIM) to compare images and identify duplicates or near-duplicates.
- **Remove Most Frequent Image**: Identifies the most frequently occurring image across the document and removes it.
- **Save Modified PDF**: Outputs a new PDF file with the watermark removed.

## Prerequisites 📋

Before you can run this script, you need to have Python installed on your machine along with the following Python libraries:
- PyMuPDF (Fitz)
- PIL (Pillow)
- NumPy
- scikit-image

You can install these dependencies using pip:
```bash
  pip install -r requirements.txt
```



## Usage 🚀

1. Place the PDF file you want to process in the same directory as the script or specify the path to the file.
2. Run the script with Python:
```bash
  python main.py
```


3. The script will process the PDF, remove the most frequent image (watermark), and save a modified version of the PDF in the same directory.

## How It Works 🛠️

1. **Extracting Images**: The script first extracts all images from the PDF.
2. **Comparing Images**: It then compares each image with every other image in the document to find duplicates based on SSIM.
3. **Identifying and Removing the Watermark**: The most frequently occurring image is considered the watermark and is removed from the document.
4. **Saving the PDF**: Finally, the script saves the modified PDF without the watermark.

## Note 📝

- The script assumes that the most frequent image in the PDF is the watermark. This might not always be the case, so use it with caution.
- The effectiveness of the watermark removal can vary based on the quality and complexity of the images in the PDF.

## Contribution 🤝

Feel free to fork this project and contribute. Whether it's adding new features, improving the documentation, or fixing bugs, your contributions are always welcome!

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.