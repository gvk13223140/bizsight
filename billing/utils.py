import qrcode
from PIL import Image
from pathlib import Path


def generate_upi_qr(
    upi_uri: str,
    bill_number: str,
    logo_path: str = None,
    output_dir: str = "media/qrcodes"
):
    """
    Generates a UPI QR code image.
    Handles bill numbers with slashes safely.
    """

    # Create base output directory
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories if bill number contains slashes
    qr_path = base_dir / bill_number
    qr_path.parent.mkdir(parents=True, exist_ok=True)

    file_path = qr_path.with_suffix(".png")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(upi_uri)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if logo_path and Path(logo_path).exists():
        logo = Image.open(logo_path)

        qr_width, qr_height = qr_img.size
        logo_size = qr_width // 4

        logo = logo.resize((logo_size, logo_size))
        pos = (
            (qr_width - logo_size) // 2,
            (qr_height - logo_size) // 2
        )

        qr_img.paste(logo, pos)

    qr_img.save(file_path)

    return str(file_path)
