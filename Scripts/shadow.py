import cv2
import numpy as np
from deepface import DeepFace

def increase_shadows(image, shadow_factor):
    """
    Increase the shadows in an image.
    
    Parameters:
    image (numpy.ndarray): Input image
    shadow_factor (float): Factor to increase shadows by (0.0 - 1.0)
    
    Returns:
    numpy.ndarray: Image with increased shadows
    """
    if image is None:
        raise ValueError("The image could not be loaded. Check the file path.")
    
    # Convert to HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Scale down the Value channel (V) to increase shadows
    hsv[:, :, 2] = hsv[:, :, 2] * shadow_factor
    
    # Convert back to BGR
    image_with_shadows = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return image_with_shadows

def extract_embedding(photo_path):
    """
    Extract facial embedding for a given photo.
    
    Parameters:
    photo_path (str): Path to the photo
    
    Returns:
    dict: Facial embedding and metadata
    """
    embedding = DeepFace.represent(img_path=photo_path, model_name='Facenet', enforce_detection=False)
    return embedding

# Load the image
image_path = 'a1.jpg'
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print(f"Error: Could not load image at path '{image_path}'. Please check the file path and ensure the file exists.")
else:
    # Extract and print face confidence before increasing shadows
    embedding_before = extract_embedding(image_path)
    confidence_before = embedding_before[0]['face_confidence']
    print(f"Face confidence before increasing shadows: {confidence_before}")
    
    # Increase shadows
    shadow_factor = 1.4  # Adjust this value to increase or decrease shadows
    image_with_shadows = increase_shadows(image, shadow_factor)

    # Save the image
    output_path = 'output.jpg'
    cv2.imwrite(output_path, image_with_shadows)

    # Extract and print face confidence after increasing shadows
    embedding_after = extract_embedding(output_path)
    confidence_after = embedding_after[0]['face_confidence']
    print(f"Face confidence after increasing shadows: {confidence_after}")

    print(f"Image with increased shadows saved as {output_path}")
