from re import search
import cv2
import numpy as np

def border_with_square_corners(input_image: str, output_image: str, color: str):
    """
    input_image: path of input file
    output_image: path of output file
    color: string hex code for color 

    return 0, 1? 
    """
    # If hex code is transparent color, change color to specific color and then change the transparency of those pixels to 0.

    if(not isHexColor(color)):
        pass


    pass

def isHexColor(color : str) -> bool:
    return search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)

def rect_with_rounded_corners(image, r, t, c):
    """
    :param image: image as NumPy array
    :param r: radius of rounded corners
    :param t: thickness of border
    :param c: color of border
    :return: new image as NumPy array with rounded corners
    """

    c += (255, )

    h, w = image.shape[:2]

    # Create new image (three-channel hardcoded here...)
    new_image = np.ones((h+2*t, w+2*t, 4), np.uint8) * 255
    new_image[:, :, 3] = 0

    # Draw four rounded corners
    new_image = cv2.ellipse(new_image, (int(r+t/2), int(r+t/2)), (r, r), 180, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(w-r+3*t/2-1), int(r+t/2)), (r, r), 270, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(r+t/2), int(h-r+3*t/2-1)), (r, r), 90, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(w-r+3*t/2-1), int(h-r+3*t/2-1)), (r, r), 0, 0, 90, c, t)

    # Draw four edges
    new_image = cv2.line(new_image, (int(r+t/2), int(t/2)), (int(w-r+3*t/2-1), int(t/2)), c, t)
    new_image = cv2.line(new_image, (int(t/2), int(r+t/2)), (int(t/2), int(h-r+3*t/2)), c, t)
    new_image = cv2.line(new_image, (int(r+t/2), int(h+3*t/2)), (int(w-r+3*t/2-1), int(h+3*t/2)), c, t)
    new_image = cv2.line(new_image, (int(w+3*t/2), int(r+t/2)), (int(w+3*t/2), int(h-r+3*t/2)), c, t)

    # Generate masks for proper blending
    mask = new_image[:, :, 3].copy()
    mask = cv2.floodFill(mask, None, (int(w/2+t), int(h/2+t)), 128)[1]
    mask[mask != 128] = 0
    mask[mask == 128] = 1
    mask = np.stack((mask, mask, mask), axis=2)

    # Blend images
    temp = np.zeros_like(new_image[:, :, :3])
    temp[(t-1):(h+t-1), (t-1):(w+t-1)] = image.copy()
    new_image[:, :, :3] = new_image[:, :, :3] * (1 - mask) + temp * mask

    # Set proper alpha channel in new image
    temp = new_image[:, :, 3].copy()
    new_image[:, :, 3] = cv2.floodFill(temp, None, (int(w/2+t), int(h/2+t)), 255)[1]

    return new_image