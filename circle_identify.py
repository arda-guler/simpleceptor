from PIL import Image

from neurons import *

def get_pixel_brightness(rgb):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    return (r + g + b)/(765) # 255 * 3 = 765

def init_AI():
    # set AI initial variables
    photocell_bias = 0.5
    identifier_bias = 5000
    photocells = []

    # create neurons
    for y in range(256):
        for x in range(256):
            new_photocell = photocell(photocell_bias)
            photocells.append(new_photocell)
    print("Initialized", len(photocells), "photocells.")

    identifier_neuron = identifier(identifier_bias, photocells)

    # create AI
    photo_intelligence = AI(photocells + [identifier_neuron])

    return photo_intelligence

def identify_image(img_path):
    image = Image.open(img_path)
    pixels = image.load()

    image_weights = Image.open("weights.png")
    pixels_weights = image_weights.load()

    f_max_weight = open("max_weight.txt", "r")
    max_weight = float(f_max_weight.read())

    def rescale_weight(pixel_weight, max_weight):
        brightness = get_pixel_brightness(pixel_weight)
        return max_weight * brightness

    photo_intelligence = init_AI()
    photo_intelligence.activate()

    # read saved weights
    for y in range(256):
        for x in range(256):
            current_neuron = photo_intelligence.get_photocell(x, y)
            current_neuron.set_weight(rescale_weight(pixels_weights[x, y], max_weight))

    # update photocell states
    for y in range(256):
        for x in range(256):
            current_neuron = photo_intelligence.get_photocell(x, y)
            current_brightness = get_pixel_brightness(pixels[x, y])
            current_neuron.update_active(current_brightness)

    # update identifier state
    ident = photo_intelligence.get_identifier()
    ident.update_active()

    print("Identification:", ident.get_active())

    photo_intelligence.deactivate()
    
def main():
    img_path = input("Image to be identified:")
    img_path = "test/" + img_path + ".png"
    identify_image(img_path)
    time.sleep(1)

main()
