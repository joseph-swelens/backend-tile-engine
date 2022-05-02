
import PIL
from src.models.bbox import Bbox
from src.models.icon import Icon
from src.models.pin import Pin
from src.models.print_format import PrintFormat
import logging

def get_leaflet_digital_pixel_size(pf : PrintFormat) -> tuple:
    # Return the sizes of the digital display. Used to calculate proportion multiplier for digital to print conversion   
    # TO DO: pull these numbers from a properties file later on so we are only updating properties files and not code
    if(pf == PrintFormat.Canvas_24_36):
        return (480, 720)
    elif (pf == PrintFormat.Canvas_20_24):
        # TO DO: this pixel convrsion. 
        return (69, 69)
    else:
        # TO DO: Exception / Logging 
        return (69, 69)


def get_print_pixel_size(pf : PrintFormat) -> tuple:
    # Return the size of print dimensions in pixels 
    # TO DO: pull these numbers from a properties file to keep code consistent when changes 

    if(pf == PrintFormat.Canvas_24_36):
        return (7200, 10800)
    elif (pf == PrintFormat.Canvas_20_24):
        # TO DO: this pixel convrsion. 
        return (69, 69)
    else:
        # TO DO: Exception / Logging 
        return (69, 69)
    pass

def get_pin_image_path(pin : Pin) -> str:
    # TO DO: change this to properties file
    output_path = ""

    if (pin.icon == Icon.CIRCLE):
        output_path = "create CIRCLE pin path"
    elif (pin.icon == Icon.HEART):
        output_path = "src/images/pins/heart_pin_500_500.png"
    else:
        # Can't find Icon
        print('cant find icon')

    return output_path


def get_pin_size(print_format: PrintFormat, pin: Pin) -> tuple:
    # convert from digital pin pixels size to print pin pixels size 
    digital_width, digital_height = get_leaflet_digital_pixel_size(print_format)
    print_width, print_height = get_print_pixel_size(print_format)

    pin_print_width = round((print_width / digital_width) * pin.digital_width)
    pin_print_height = round((print_height / digital_height) * pin.digital_height)

    return (pin_print_width, pin_print_height)

def get_pin_location(map_box: Bbox, pin: Pin, print_format: PrintFormat) -> tuple:
    # Convert digital pin location (lon, lat) to print pin location (pixels)
    
    #Check point is in bbox.
    if(not map_box.contains(pin.location)):
        print('pin not in box')
    
    # Calculate bbox total x & y value
    total_x_bbox = map_box.get_total_x_length()
    total_y_bbox = map_box.get_total_y_length()

    # Calculate the x & y pixel location of pin on print image
    pf_width, pf_height = get_print_pixel_size(print_format)
    x_pixel_location = round(abs(((pin.location.lon - map_box.top_left.lon) / total_x_bbox) * pf_width))
    y_pixel_location = round(abs(((pin.location.lat - map_box.top_left.lat) / total_y_bbox) * pf_height))
    logging.info("print width: " + str(pf_width) + " height: " + str(pf_height))
    logging.info("\tpixel location before pin image adjustment")
    logging.info("\tpixel location of pin x: " + str(x_pixel_location) + " y: " + str(y_pixel_location))

    # TO DO: Delete this
    # REd Line for pre adjusted 
    map_img = PIL.Image.open("all_skate_image.png")
    draw = PIL.ImageDraw.Draw(map_img)
    draw.line(((x_pixel_location, y_pixel_location), (x_pixel_location, y_pixel_location+1000)), fill=(255, 0, 0))
    draw.line(((x_pixel_location, y_pixel_location), (x_pixel_location+1000, y_pixel_location)), fill=(255, 0, 0))
    

    # Adjust for where the pin should actually go on print image 
    adj_x_pixels = round(x_pixel_location - (get_pin_size(print_format, pin)[0] * .5))
    adj_y_pixels = round(y_pixel_location - (get_pin_size(print_format, pin)[1]))
    logging.info("pin image location after adjustment")
    logging.info("\tlocation pin image paste x: " + str(adj_x_pixels) + " y: " + str(adj_y_pixels))
    

    # TO DO: Delete this
    #Blue lines intersection for adjusted new location of "picture".  
    draw = PIL.ImageDraw.Draw(map_img)
    draw.line(((adj_x_pixels, adj_y_pixels), (adj_x_pixels, adj_y_pixels+1000)), fill=(0, 0, 255))
    draw.line(((adj_x_pixels, adj_y_pixels), (adj_x_pixels + 1000, adj_y_pixels)), fill=(0, 0, 255))
    map_img.save("locationColors.png")

    return (adj_x_pixels, adj_y_pixels)

