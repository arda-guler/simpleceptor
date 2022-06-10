import os
import random
import glob
import time
from PIL import Image

from neurons import *

def clear_cmd_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def get_images_in_dir(directory):
    str_search = directory + "/*.png"
    return glob.glob(str_search)

def load_image(img_path):
    image = Image.open(img_path)
    pixels = image.load()

    return image, pixels

def get_pixel_brightness(rgb):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    return (r + g + b)/(765) # 255 * 3 = 765
        
def autotrain(target_accuracy_percent, min_steps=500):
    clear_cmd_terminal()

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
    photo_intelligence.activate()
    time.sleep(1)

    # get image directory
    img_dir = "images"
    imgs = get_images_in_dir(img_dir)

    run_step = 0
    correct_ids = 0
    while photo_intelligence.get_active():
        run_step += 1
        clear_cmd_terminal()
        
        print("\n-------------")
        print("Step:", run_step)
        print("Current accuracy:" + str((correct_ids/run_step)*100) + "%")

        image_path = random.choice(imgs)
        print("Now looking at: " + image_path)
        current_image, pixels = load_image(image_path)

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
        is_circle = bool(image_path.startswith("images\circle"))
        
        is_correct = False
        if (is_circle and ident.get_active()) or (not is_circle and not ident.get_active()):
            is_correct = True

        print("Is identification correct:", is_correct)

        incr = 1

        if ident.get_active() and is_correct:
            # correctly identified as True
            correct_ids += 1
            
        elif ident.get_active() and not is_correct:
            # wrongly identified as True
            for pc in photocells:
                if pc.get_active():
                    pc.decreaseWeight(incr)
                    
        elif (not ident.get_active()) and is_correct:
            # correctly identified as False
            correct_ids += 1
                    
        else:
            # wrongly identified as False
            for pc in photocells:
                if pc.get_active():
                    pc.increaseWeight(incr)

        if (correct_ids/run_step)*100 >= target_accuracy_percent and run_step >= min_steps:
            photocell_weights = photo_intelligence.get_photocellWeights()
            save_image = Image.new(mode="RGB", size=(256,256))
            save_pixels = save_image.load()
            max_weight = max(photocell_weights)
            for y in range(256):
                for x in range(256):
                    save_brightness = int((photocell_weights[y * 256 + x]/max_weight) * 255)
                    save_pixels[x, y] = (save_brightness, save_brightness, save_brightness)

            save_image.save("weights.png")
            print("Max weight:", max_weight)

            with open("max_weight.txt", "w") as f_txt:
                f_txt.write(str(max_weight))
                
            return photo_intelligence

def main():
    photo_intelligence = autotrain(96, 150)
    photo_intelligence.deactivate()
    time.sleep(5)

main()
