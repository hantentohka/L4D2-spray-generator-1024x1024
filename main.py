import os
import subprocess
from PIL import Image
import argparse

landscape = False
parser = argparse.ArgumentParser(description="Process an input file.")
parser.add_argument("input_path", help="Path to the input file")
args = parser.parse_args()
#input_image_path = "G:\\Python_Projects\\vtf_convert\\116614094_p2.png".replace("\\","/")
input_image_path = str(args.input_path).replace("\\", "/")
image_folder = '/'.join(input_image_path.split("/")[:-1]) + '/'
file_name = (input_image_path.split("/")[-1]).split(".")[0]
print(f"Input image: {input_image_path}\n")

def resize_and_center_image(original_png_path):
    output_path = image_folder + "resized_" + file_name + ".png"
    with Image.open(original_png_path) as img:
        # Get the original width and height of the image
        original_width, original_height = img.size

        # Determine the scaling factor
        if original_width >= original_height:
            # Image is wider than tall or square
            global landscape
            landscape = True
            scaling_factor = 1024 / float(original_width)
        else:
            # Image is taller than wide
            scaling_factor = 1024 / float(original_height)

        # Calculate the new width and height
        temp_width = int(original_width * scaling_factor)
        if temp_width == 1023 or temp_width == 1025:
            temp_width = 1024
        temp_height = int(original_height * scaling_factor)
        if temp_height == 1023 or temp_height == 1025:
            temp_height = 1024

        # If image is square
        if temp_width == temp_height:
            temp_width = 1020

        # Resize the image
        resized_image = img.resize((temp_width, temp_height), Image.LANCZOS)

        # Calculate the new canvas size and paste position
        if temp_width == 1024:
            new_width, new_height = 1024, 1020
            paste_position = ((new_width - temp_width) // 2, 0)
        elif temp_height == 1024:
            new_width, new_height = 1020, 1024
            paste_position = (0, (new_height - temp_height) // 2)
        else:
            raise ValueError("Input image size must be either 1024xN or Nx1024.")

        # Create a new blank image with the new canvas size and make it transparent
        new_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

        # Calculate the paste position to center the original image on the new canvas
        paste_position = ((new_width - temp_width) // 2, (new_height - temp_height) // 2)

        # Paste the original image onto the new canvas
        new_img.paste(resized_image, paste_position)

        # Save the new image with transparency
        new_img.save(output_path)
        print("Resizing of the input image completed.\n")

        return output_path

def image_to_dds(resized_image_path):
    output_path = image_folder + file_name + ".dds"
    default_executable_path = "C:\\Program Files\\NVIDIA Corporation\\NVIDIA Texture Tools\\nvcompress.exe"
    executable_path = default_executable_path
    if not os.path.exists(default_executable_path):
        executable_path = "nvcompress.exe"
    try:
        subprocess.run([executable_path, "-rgb", "-bc1a", "-nomips", resized_image_path, output_path], check=True)
        print("Conversion successful!")
    except subprocess.CalledProcessError as e:
        print("Conversion failed:", e)
        print(f"Most likely NVIDIA Texture Tools isn't installed in the default location {default_executable_path} or "
              f"environment parmeters for the executables isn't set properly. Run nvcompress.exe from command line to "
              f"check if it works.")
    return output_path

def dds_to_vtf(dds_image_path):
    output_path = image_folder + file_name + ".vtf"
    hex_string = "56 54 46 00 07 00 00 00 01 00 00 00 40 00 00 00 FC 03 00 04 00 03 00 00 01 00 00 00 78 00 1A 02 00 6C 1C 3F 9F A4 C6 3E 24 BD A2 3E 05 FF 57 7C 00 00 80 3F 0D 00 00 00 01 0D 00 00 00 FE 00 01"
    # Remove spaces and convert to bytes
    if landscape:
        hex_string = "56 54 46 00 07 00 00 00 01 00 00 00 40 00 00 00 00 04 FC 03 00 03 00 00 01 00 00 00 78 00 1A 02 00 6C 1C 3F 9F A4 C6 3E 24 BD A2 3E 05 FF 57 7C 00 00 80 3F 0D 00 00 00 01 0D 00 00 00 00 FE 01"
    hex_bytes = bytes.fromhex(hex_string.replace(" ", ""))

    # Read the DDS file as binary
    with open(dds_image_path, "rb") as dds_file:
        dds_content = dds_file.read()

    part_to_remove = bytes.fromhex("44 44 53 20 7C 00 00 00 07 10 08 00 00 04 00 00 FC 03 00 00 00 F8 07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 20 00 00 00 04 00 00 00 44 58 54 31 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

    # Remove the part from dds_content
    dds_content = dds_content[len(part_to_remove):]

    # Combine hex bytes and DDS content
    combined_data = hex_bytes + dds_content

    # Write the combined data to a new file
    with open(output_path, "wb") as output_file:
        output_file.write(combined_data)
    print(f"\nConversion of the file to dds successful. Image saved to {output_path}")


resized_image_path = resize_and_center_image(input_image_path)
dds_path = image_to_dds(resized_image_path)
dds_to_vtf(dds_path)

os.remove(resized_image_path)
os.remove(dds_path)
input("Press Enter to exit...")  # Wait for user input before exiting