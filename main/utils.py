from django.core.exceptions import ValidationError
from PIL import Image
import magic


def validate_image(file):
    try:
        # Check for common image formats
        img = Image.open(file)
        img.verify()
        print("Raster image validation passed.")
        # Reset file pointer to beginning
        file.seek(0)
    except (IOError, SyntaxError):
        # Check if the file is an SVG
        file.seek(0)
        mime = magic.from_buffer(file.read(), mime=True)
        print(f"MIME type: {mime}")
        if mime != 'image/svg+xml':
            raise ValidationError("Upload a valid image. The file you uploaded was either not an image or a "
                                  "corrupted image.")
        print("SVG image validation passed.")
        # Reset file pointer to beginning again for further use
        file.seek(0)
