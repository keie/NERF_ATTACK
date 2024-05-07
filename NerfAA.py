
# # -----------------Adversarial Attacks-----------
# # --------------- on Nerfs and Generfs ----------
# #           By Hugo SOSAPAVON & Kevin NAVA
# # 

# import os
# import random
# from shutil import copy2

# import matplotlib.colors  # Needed for color space conversions
# import numpy as np
# from IPython.display import display
# from PIL import Image

# input_dataset =  r"D:\Instant-NGP-for-RTX-2000\data\nerf\Normal\lego\val"
# output_dataset = r"D:\Instant-NGP-for-RTX-2000\data\nerf\Attacked\lego\val"


# # --------------------------    MAIN  ---------------------------------------

# def main():
#     modify_images(input_dataset,output_dataset) 

# # --------------------------------- FUNCTION TO MODIFY THE FOLDER ----------------
# #con logeo solamente 
# def modify_images(source_folder, target_folder, percentage=50):
#     # Ensure the source folder exists
#     if not os.path.exists(source_folder):
#         print("The source folder does not exist.")
#         return
    
#     # Ensure the target folder exists, create it if it doesn't
#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)
#         print(f"Created target folder at {target_folder}")

#     # Loop through each file in the source directory
#     for filename in os.listdir(source_folder):
#         source_file_path = os.path.join(source_folder, filename)
#         target_file_path = os.path.join(target_folder, filename)

#         # Check if the file is an image
#         if source_file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
#             try:
#                 # Decide randomly whether to modify this image based on the percentage
#                 if random.random() < (percentage / 100.0) and filename != "r_35.jpg":
#                     # Open and modify selected images
#                     with Image.open(source_file_path) as img:

#                         # -------------     ATACKS GO HERE--------------
#                         #modified_img = img
#                         #modified_img = add_color_noise_to_image(img)
#                         modified_img = random_center_crop(img)


#                         # -------------------------------------
#                         modified_img.save(target_file_path)
#                         print(f"Modified and saved {filename} to {target_folder}")
#                 else:
#                     # Copy unmodified images directly
#                     copy2(source_file_path, target_file_path)
#                     print(f"Copied unmodified {filename} to {target_folder}")

#             except Exception as e:
#                 print(f"Failed to process {filename}. Error: {e}")
#         else:
#             print(f"Skipped {filename}, not an image file.")





# #################################     Attack Functions    ############################

# # ------------------------------------- NOISE ATTACKS ------------------------
# def add_noise_to_image(image, percentage=15):
#     # Convert the image to a numpy array
#     data = np.array(image)
    
#     # Determine the number of pixels to modify based on the percentage
#     total_pixels = data.size
#     pixels_to_modify = int(total_pixels * percentage / 100)
    
#     # Generate random indices to select which pixels to modify
#     # Note: np.unravel_index converts flat indices to coordinate indices for the given shape
#     indices = np.unravel_index(
#         np.random.choice(range(total_pixels), size=pixels_to_modify, replace=False),
#         data.shape
#     )
    
#     # Generate random noise
#     # Adjust the noise range and data type according to the image type
#     noise = np.random.randint(0, 255, pixels_to_modify, dtype='uint8')
    
#     # Apply noise only to the selected pixels
#     # For color images, apply noise uniformly across all channels to keep color consistency
#     if data.ndim == 3:
#         for channel in range(data.shape[2]):
#             data[indices[0], indices[1], channel] = np.clip(data[indices[0], indices[1], channel] + noise, 0, 255)
#     else:
#         data[indices] = np.clip(data[indices] + noise, 0, 255)

#     # Convert the numpy array back to an Image object
#     return Image.fromarray(data)


# # ----------------------------- COLORS NOISE ----------------------------------
# def add_color_noise_to_image(image, percentage=15):
#     # Convert the image to a numpy array
#     data = np.array(image)
    
#     # Determine the number of pixels to modify based on the percentage
#     total_pixels = data.size // data.shape[-1]  # Correctly calculate number of pixels for color images
#     pixels_to_modify = int(total_pixels * percentage / 100)
    
#     # Generate random indices to select which pixels to modify
#     # np.unravel_index converts flat indices to coordinate indices for the given shape
#     indices = np.unravel_index(
#         np.random.choice(range(total_pixels), size=pixels_to_modify, replace=False),
#         (data.shape[0], data.shape[1])
#     )
    
#     # Generate random noise for each color channel
#     if data.ndim == 3:  # Color image
#         noise = np.random.randint(0, 256, (pixels_to_modify, 3), dtype='uint8')
#         for channel in range(3):  # Apply different noise to each channel
#             data[indices[0], indices[1], channel] = np.clip(data[indices[0], indices[1], channel] + noise[:, channel], 0, 255)
#     else:  # Grayscale image
#         noise = np.random.randint(0, 256, pixels_to_modify, dtype='uint8')
#         data[indices] = np.clip(data[indices] + noise, 0, 255)

#     # Convert the numpy array back to an Image object
#     return Image.fromarray(data)


# # --------------------------- ILLUMINATION CHANGE --------------------------
# def change_illumination_randomly(image, min_factor=-0.2, max_factor=0.2):
#     # Randomly choose a change factor within the specified range
#     change_factor = random.uniform(min_factor, max_factor)
    
#     # Convert the image to a numpy array
#     data = np.array(image)
    
#     # Handle the alpha channel for PNGs
#     has_alpha = data.shape[-1] == 4
#     if has_alpha:
#         alpha_channel = data[:, :, 3]
#         data = data[:, :, :3]
    
#     # Convert RGB to HSV and adjust the brightness
#     hsv_image = matplotlib.colors.rgb_to_hsv(data / 255.0)
#     hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + change_factor, 0, 1)
    
#     # Convert back to RGB
#     new_rgb_image = matplotlib.colors.hsv_to_rgb(hsv_image) * 255
#     if has_alpha:
#         new_rgb_image = np.concatenate((new_rgb_image, alpha_channel[:, :, None]), axis=-1)
    
#     new_image = Image.fromarray(new_rgb_image.astype('uint8'))
#     return new_image

# # --------------------------- ILLUMINATION CHANGE --------------------------
# def change_illumination_randomly(image, min_factor=-0.2, max_factor=0.2):
#     # Randomly choose a change factor within the specified range
#     change_factor = random.uniform(min_factor, max_factor)
    
#     # Convert the image to a numpy array
#     data = np.array(image)
    
#     # Handle the alpha channel for PNGs
#     has_alpha = data.shape[-1] == 4
#     if has_alpha:
#         alpha_channel = data[:, :, 3]
#         data = data[:, :, :3]
    
#     # Convert RGB to HSV and adjust the brightness
#     hsv_image = matplotlib.colors.rgb_to_hsv(data / 255.0)
#     hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + change_factor, 0, 1)
    
#     # Convert back to RGB
#     new_rgb_image = matplotlib.colors.hsv_to_rgb(hsv_image) * 255
#     if has_alpha:
#         new_rgb_image = np.concatenate((new_rgb_image, alpha_channel[:, :, None]), axis=-1)
    
#     new_image = Image.fromarray(new_rgb_image.astype('uint8'))
#     return new_image
# # ------------------------- RANDOM CROP  -----------------------------------
# def random_center_crop(img):
#     """
#     Crop a random part from the center of the image with random dimensions.
    
#     Args:
#     img (PIL.Image): The image to crop.

#     Returns:
#     PIL.Image: The cropped image.
#     """
#     width, height = img.size

#     # Determine random dimensions for the crop (at least 50% and at most 90% of the original dimensions)
#     crop_width = random.randint(width // 2, int(width * 0.9))
#     crop_height = random.randint(height // 2, int(height * 0.9))

#     # Calculate the top-left point of the crop area to center the crop
#     left = (width - crop_width) // 2
#     top = (height - crop_height) // 2
#     right = left + crop_width
#     bottom = top + crop_height

#     # Crop the image
#     cropped_image = img.crop((left, top, right, bottom))

#     return cropped_image


# # Definicion del Main
# if __name__ == "__main__":
#     main()




import os
import random
from shutil import copy2
import matplotlib.colors
import numpy as np
from PIL import Image

input_root = "/Users/appleuser/Desktop/uam/TRDP/pres3/TRDP-IPCV/datasetsNerf"
output_root = "/Users/appleuser/Desktop/uam/TRDP/pres3/TRDP-IPCV/datasetsNerf/Attacked"

# Define attack types for folder creation
attack_types = ["color_noise", "illumination_change", "random_crop"]

def main():
    datasets = ['lego', 'house1', 'fox']  # You can add more datasets here
    for dataset in datasets:
        input_dataset = os.path.join(input_root, dataset, "images")
        for attack in attack_types:
            output_dataset = os.path.join(output_root, dataset, f"{dataset}AttackedBy{attack.capitalize()}")
            if not os.path.exists(output_dataset):
                os.makedirs(output_dataset)
                print(f"Created target folder at {output_dataset}")

            # Modify images using different attack methods
            if attack == "color_noise":
                modify_images(input_dataset, output_dataset, add_color_noise_to_image)
            elif attack == "illumination_change":
                modify_images(input_dataset, output_dataset, change_illumination_randomly)
            elif attack == "random_crop":
                modify_images(input_dataset, output_dataset, random_center_crop)

def modify_images(source_folder, target_folder, attack_function):
    # Loop through each file in the source directory
    for filename in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, filename)
        target_file_path = os.path.join(target_folder, filename)

        # Check if the file is an image and not the specific excluded file
        if source_file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')) and filename.lower() != "r_35.png":
            try:
                with Image.open(source_file_path) as img:
                    modified_img = attack_function(img)
                    modified_img.save(target_file_path)
                    print(f"Modified and saved {filename} to {target_folder}")
            except Exception as e:
                print(f"Failed to process {filename}. Error: {e}")
        else:
            # This will print a message for non-image files and the excluded image
            if filename.lower() == "r_35.png":
                print(f"Excluded {filename} from modification.")
            else:
                print(f"Skipped {filename}, not an image file.")

def add_color_noise_to_image(image, percentage=15):
    data = np.array(image)
    total_pixels = data.size // data.shape[-1]
    pixels_to_modify = int(total_pixels * percentage / 100)
    indices = np.unravel_index(np.random.choice(range(total_pixels), size=pixels_to_modify, replace=False),
                               (data.shape[0], data.shape[1]))
    noise = np.random.randint(0, 256, (pixels_to_modify, 3), dtype='uint8')
    for channel in range(3):
        data[indices[0], indices[1], channel] = np.clip(data[indices[0], indices[1], channel] + noise[:, channel], 0, 255)
    return Image.fromarray(data)

def change_illumination_randomly(image, min_factor=-0.2, max_factor=0.2):
    change_factor = random.uniform(min_factor, max_factor)
    data = np.array(image)
    has_alpha = data.shape[-1] == 4
    if has_alpha:
        alpha_channel = data[:, :, 3]
        data = data[:, :, :3]
    hsv_image = matplotlib.colors.rgb_to_hsv(data / 255.0)
    hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + change_factor, 0, 1)
    new_rgb_image = matplotlib.colors.hsv_to_rgb(hsv_image) * 255
    if has_alpha:
        new_rgb_image = np.concatenate((new_rgb_image, alpha_channel[:, :, None]), axis=-1)
    return Image.fromarray(new_rgb_image.astype('uint8'))

def random_center_crop(img):
    width, height = img.size
    crop_width = random.randint(width // 2, int(width * 0.9))
    crop_height = random.randint(height // 2, int(height * 0.9))
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    cropped_image = img.crop((left, top, right, bottom))
    return cropped_image

if __name__ == "__main__":
    main()
