import os
import subprocess
from PIL import Image
import argparse
import gif_to_vtf

VTF_128_ONE_FRAME_SIZE = 9
VTF_256_ONE_FRAME_SIZE = 34
VTF_512_ONE_FRAME_SIZE = 130

vtf_size_dict = {128: VTF_128_ONE_FRAME_SIZE, 256: VTF_256_ONE_FRAME_SIZE, 512: VTF_512_ONE_FRAME_SIZE,}
landscape = False
parser = argparse.ArgumentParser(description="Process an input file.")
parser.add_argument("input_path", help="Path to the input file")
args = parser.parse_args()


def extract_image_folder(full_path):
    return '/'.join(full_path.split("/")[:-1]) + '/'
def extract_image_filename(full_path):
    return (full_path.split("/")[-1]).split(".")[0]

# input_image_path = "G:\\Python_Projects\\vtf_convert\\full.jpg".replace("\\","/")
# input_image_path = "G:\\Python_Projects\\vtf_convert\\bounce.gif".replace("\\","/")
input_image_path = str(args.input_path).replace("\\", "/")
image_folder = extract_image_folder(input_image_path)
file_name = extract_image_filename(input_image_path)
print(f"Input image: {input_image_path}\n")


def resize_and_center_image(original_png_path, width=1024, height=1020, GIF=False):
    output_path = image_folder + "resized_" + file_name + ".png"
    if GIF:
        output_path = extract_image_folder(original_png_path) + "resized_" + extract_image_filename(original_png_path) + ".png"
    with Image.open(original_png_path) as img:
        # Get the original width and height of the image
        original_width, original_height = img.size
        bigger_dimension , smaller_dimension = [width, height] if width >= height else [height, width]

        # Determine the scaling factor
        if original_width >= original_height:
            # Image is wider than tall or square
            global landscape
            if original_width > original_height:
                landscape = True
            scaling_factor = bigger_dimension / float(original_width)
        else:
            # Image is taller than wide
            scaling_factor = bigger_dimension / float(original_height)

        # Calculate the new width and height
        temp_width = int(original_width * scaling_factor)
        if temp_width == width - 1 or temp_width == width + 1:
            temp_width = width
        temp_height = int(original_height * scaling_factor)
        if temp_height == height - 1 or temp_height == height + 1:
            temp_height = height

        # If image is square
        if temp_width == temp_height:
            temp_width = smaller_dimension

        # Resize the image
        resized_image = img.resize((temp_width, temp_height), Image.LANCZOS)

        # Calculate the new canvas size and paste position
        if temp_width == bigger_dimension:
            new_width, new_height = bigger_dimension, smaller_dimension
            paste_position = ((new_width - temp_width) // 2, 0)
        elif temp_height == bigger_dimension:
            new_width, new_height = smaller_dimension, bigger_dimension
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


def image_to_dds(resized_image_path, GIF=False):
    output_path = image_folder + file_name + ".dds"
    if GIF:
        output_path = extract_image_folder(resized_image_path) + extract_image_filename(resized_image_path) + ".dds"
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

    part_to_remove = bytes.fromhex(
        "44 44 53 20 7C 00 00 00 07 10 08 00 00 04 00 00 FC 03 00 00 00 F8 07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 20 00 00 00 04 00 00 00 44 58 54 31 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

    # Remove the part from dds_content
    dds_content = dds_content[len(part_to_remove):]

    # Combine hex bytes and DDS content
    combined_data = hex_bytes + dds_content

    # Write the combined data to a new file
    with open(output_path, "wb") as output_file:
        output_file.write(combined_data)
    print(f"\nConversion of the file to dds successful. Image saved to {output_path}")


def gif_to_jpg(gif_path):
    gif = Image.open(gif_path)

    frame_number = 0
    frame_paths = []
    while True:
        try:
            # Seek to the correct frame
            gif.seek(frame_number)
        except EOFError:
            break  # End of sequence

        # Construct the output file path
        png_path = os.path.join(image_folder, f"{file_name}_frame_{frame_number}.jpg")

        # Save the current frame as PNG
        gif.convert("RGB").save(png_path, "PNG")

        frame_number += 1

        frame_paths.append(png_path)

    return frame_paths


def get_frames_summing_under_512KB(all_vtf_frames, size):
    frame_size_KB = vtf_size_dict[size]
    original_frame_count = len(all_vtf_frames)
    current_frame_count = original_frame_count
    while current_frame_count * frame_size_KB > 511:
        current_frame_count -= 1
    step = original_frame_count / current_frame_count
    selected_frames = [int(i * step) for i in range(current_frame_count)]
    selected_vtf_frames = [all_vtf_frames[i] for i in selected_frames]
    return selected_vtf_frames


def generate_vtf(size):
    resized_frame_paths = [resize_and_center_image(frame_path,size, size, GIF=True) for frame_path in frame_paths]
    dds_paths = [image_to_dds(dds_path, GIF=True) for dds_path in resized_frame_paths]
    dxt1_images = [gif_to_vtf.read_dxt1_image(dds_path) for dds_path in dds_paths]
    dxt_images_trimmed = get_frames_summing_under_512KB(dxt1_images, size)
    vtf_data = gif_to_vtf.create_vtf(dxt_images_trimmed, size)
    gif_to_vtf.write_vtf(vtf_data, image_folder + file_name + "_" + str(size) + ".vtf")
    [os.remove(resized_frame_path) for resized_frame_path in resized_frame_paths]
    [os.remove(dds_path) for dds_path in dds_paths]


if input_image_path.endswith(".gif"):
    frame_paths = gif_to_jpg(input_image_path)
    generate_vtf(128)
    generate_vtf(256)
    generate_vtf(512)
    [os.remove(frame_path) for frame_path in frame_paths]
else:
    resized_image_path = resize_and_center_image(input_image_path)
    dds_path = image_to_dds(resized_image_path)
    dds_to_vtf(dds_path)

    os.remove(resized_image_path)
    os.remove(dds_path)
    input("Press Enter to exit...")
