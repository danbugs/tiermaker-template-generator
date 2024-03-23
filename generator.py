import argparse
from PIL import Image, ImageDraw, ImageFont
import os

def resize_and_crop_center(img, target_size=(800, 800)):
    img.thumbnail((target_size[0] * 2, target_size[1] * 2), Image.LANCZOS)
    width, height = img.size
    left = (width - target_size[0]) / 2
    top = (height - target_size[1]) / 2
    right = (width + target_size[0]) / 2
    bottom = (height + target_size[1]) / 2
    img = img.crop((left, top, right, bottom))
    return img

def add_text_to_image(image_path, text, output_folder):
    with Image.open(image_path) as img:
        img = resize_and_crop_center(img)
        draw = ImageDraw.Draw(img)
        
        # Since the image is scaled, we're doubling the size of the font and rectangle dimensions
        font_size = int(min(img.size) * 0.2)  # Increase initial percentage
        font = ImageFont.truetype("arialbd.ttf", font_size)
        
        text_width = draw.textlength(text, font=font)
        text_height = font_size
        
        while text_width > img.width - 80:  # Increased padding for larger text
            font_size -= 4  # More aggressive adjustment for larger sizes
            font = ImageFont.truetype("arialbd.ttf", font_size)
            text_width = draw.textlength(text, font=font)
        
        rectangle_margin = 40  # Increased margin for the larger rectangle
        rectangle_y_start = img.height - text_height - (2 * rectangle_margin)
        rectangle_end = (img.width - 40, img.height - 40)  # Adjusted for increased padding
        
        draw.rectangle([(40, rectangle_y_start), rectangle_end], fill="yellow")
        
        text_position = (40 + rectangle_margin, rectangle_y_start + rectangle_margin)  # Adjusted text position
        
        draw.text(text_position, text, font=font, fill="black")
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        new_image_path = os.path.join(output_folder, os.path.basename(image_path))
        img.save(new_image_path)

def process_folder(folder_path):
    output_folder = os.path.join(folder_path, "images_with_text")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            text = os.path.splitext(filename)[0]
            file_path = os.path.join(folder_path, filename)
            add_text_to_image(file_path, text, output_folder)

def main():
    parser = argparse.ArgumentParser(description='Add filenames as text overlay to images.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing images.')
    
    args = parser.parse_args()
    process_folder(args.folder_path)

if __name__ == "__main__":
    main()
