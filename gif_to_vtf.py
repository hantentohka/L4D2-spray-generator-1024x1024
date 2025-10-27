import struct


def create_vtf_header(size, gif_frame_no, mipmaps = 1):
    # Define the values for the VTF header
    signature = b'VTF\0'             # File signature ("VTF\0")
    version = [7, 1]                 # Version (major, minor)
    headerSize = 64                  # Size of the header struct (80 bytes)
    width = size                      # Width of the largest mipmap in pixels
    height = size                     # Height of the largest mipmap in pixels
    flags = 0x000300                        # VTF flags (you should set appropriate flags)
    frames = gif_frame_no                       # Number of frames, if animated
    firstFrame = 0                   # First frame in animation (0 based)
    padding0 = b'\0\0\0\0'           # Reflectivity padding (4 bytes)
    reflectivity = [0x00, 0xFFFFFFFF, 0x3EC6A49F]   # Reflectivity vector (3 floats)
    padding1 = b'\0\0\0\0'           # Reflectivity padding (4 bytes)
    bumpmapScale = 0xFF             # Bumpmap scale (float)
    highResImageFormat = 0x7C57FF05           # High resolution image format (int)
    mipmapCount = 0x00                 # Number of mipmaps (unsigned char)
    lowResImageFormat = 0x0D3F8000           # Low resolution image format (int, usually DXT1)
    lowResImageWidth = 0             # Low resolution image width (unsigned char)
    lowResImageHeight = 0            # Low resolution image height (unsigned char)
    depth = 0x0D01                        # Depth of the largest mipmap in pixels (unsigned short)
    padding2 = b'\0\0\0'             # Depth padding (3 bytes)
    numResources = 0x0100FE                 # Number of resources this VTF has (unsigned int)
    padding3 = b'\0\0\0\0\0\0\0\0'   # Padding for alignment (8 bytes)

    if mipmaps != 1:
        flags = 0x000200
    vtf_header = struct.pack(
        #'4s 2I I 2H I 2H 4x 3f 4x f i B i B B H 3x I 4x',
        #'=4s 2I I 2H I 2H 3f f i B i B B x H 2x I',
        '=4s 2I I 2H I 2H',
        signature,                  # '4s' for 4-byte signature
        version[0], version[1],     # '2I' for two 4-byte unsigned integers
        headerSize,                 # 'I' for 4-byte unsigned integer
        width, height,              # '2H' for two 2-byte unsigned shorts
        flags,                      # 'I' for 4-byte unsigned integer
        frames, firstFrame,         # '2H' for two 2-byte unsigned shorts
        # #padding0,                   # '4s' for 4-byte padding
        # reflectivity[0], reflectivity[1], reflectivity[2],  # '3f' for three 4-byte floats
        # #padding1,                   # '4s' for 4-byte padding
        # bumpmapScale,               # 'f' for 4-byte float
        # highResImageFormat,         # 'i' for 4-byte signed integer
        # mipmapCount,                # 'B' for 1-byte unsigned char
        # lowResImageFormat,          # 'i' for 4-byte signed integer
        # lowResImageWidth,           # 'B' for 1-byte unsigned char
        # lowResImageHeight,          # 'B' for 1-byte unsigned char
        # depth,                      # 'H' for 2-byte unsigned short
        # #padding2,                   # '3x' for 3 bytes of padding
        # numResources,               # 'I' for 4-byte unsigned integer
        # #padding3                    # '8x' for 8 bytes of padding
    )
    hex_string = f"78 00 1A 02 00 6C 1C 3F 9F A4 C6 3E 23 BD A2 3E 05 FF 57 7C 00 00 80 3F 0D 00 00 00 0{mipmaps} 0D 00 00 00 FE 00 BA"
    hex_bytes = bytes.fromhex(hex_string.replace(" ", ""))
    return vtf_header + hex_bytes

def create_vtf(dxt1_images, size=128, mipmaps = 1):
    VTF_HEADER_SIZE = 80  # 80 bytes for the header

    if mipmaps == 1:
        gif_frame_no = len(dxt1_images)
    else:
        gif_frame_no = 1
    # Create the VTF header
    header = create_vtf_header(size, gif_frame_no, mipmaps= mipmaps)

    #assert len(header) == VTF_HEADER_SIZE, f"Header size is {len(header)} bytes, expected {VTF_HEADER_SIZE} bytes."

    # Combine the header and the DXT1 image data
    vtf_data = bytearray(header)

    if mipmaps == 1:
        for image in dxt1_images:
            vtf_data.extend(image)
    else:
        for image in dxt1_images[::-1]:
            vtf_data.extend(image)

    return vtf_data


def read_dxt1_image(file_path):
    with open(file_path, 'rb') as f:
        dds_content = f.read()
        part_to_remove = bytes.fromhex(
            "44 44 53 20 7C 00 00 00 07 10 08 00 00 04 00 00 FC 03 00 00 00 F8 07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 20 00 00 00 04 00 00 00 44 58 54 31 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

        # Remove the part from dds_content
        dds_content = dds_content[len(part_to_remove):]
        return dds_content


def write_vtf(vtf_data, output_vtf_filename):
    with open(output_vtf_filename, 'wb') as f:
        f.write(vtf_data)


print("VTF file created successfully.")
