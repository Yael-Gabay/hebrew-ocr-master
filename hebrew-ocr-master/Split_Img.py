import cv2
import pytesseract
import os

# Read the input image

def perform_ocr(image_path: str) -> None:
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR to extract text and bounding boxes
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    # Set the output folder name
    output_folder = 'images_after_splitting'

    # Check if the output folder already exists
    if not os.path.exists(output_folder):
        # If the folder doesn't exist, create it
        os.makedirs(output_folder)

    # Initialize a counter for words
    word_counter = 0

    # Define the expansion factor for the bounding box (in pixels)
    expansion_factor = 12  # Adjust this value as needed

    # Iterate over each word bounding box
    for i, word_text in reversed(list(enumerate(data['text']))):
        # Filter out non-word regions (ignore empty strings)
        if word_text.strip():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            
            # Expand the bounding box coordinates
            x -= expansion_factor
            y -= expansion_factor
            w += 2 * expansion_factor
            h += 2 * expansion_factor
            
            # Ensure the coordinates are within the image boundaries
            x = max(0, x)
            y = max(0, y)
            w = min(w, image.shape[1] - x)
            h = min(h, image.shape[0] - y)
            
            # Crop the region corresponding to the expanded bounding box
            word_image = image[y:y+h, x:x+w]

            resized_word_image = cv2.resize(word_image, (128, 32))
            
            # Save the word image into the folder
            cv2.imwrite(os.path.join(output_folder, f'word_{word_counter}.jpg'), resized_word_image)

            # Print the text of each word along with its expanded bounding box coordinates
            print(f"Word {word_counter}: {word_text}, Expanded Bounding Box: (x={x}, y={y}, w={w}, h={h})")
            
            # Increment the word counter
            word_counter += 1