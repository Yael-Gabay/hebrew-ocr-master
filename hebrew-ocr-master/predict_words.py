from HebHTR import *
from bidi.algorithm import get_display
import tensorflow as tf
import shutil
import os

folder_path = "/tmp/images_after_splitting"


def perform_ocr():
    new_word = ""
    # Loop through all files in the folder
    for filename in sorted(os.listdir(folder_path)):
        # Check if the file is an image (you may need to adjust this condition based on your file extensions)
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Process the image file
            filename = os.path.join(folder_path, filename)

            img = HebHTR(filename)
            tf.reset_default_graph()
            print(img)
            text = img.imgToWord(iterations=5, decoder_type='word_beam')

            new_word += text[0][::-1]
            new_word += " "
            # Add your code to process the image here
    words = new_word.split(" ")
    hebrew_word = " ".join(get_display(x) for x in words)

    # Delete all crated images
    shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)


    return hebrew_word





