from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import mm
from pathlib import Path
from django.conf import settings
import os

NAVY = HexColor("#0A1F44")
IVORY = HexColor("#F9F6F1")
LIGHT_GRAY = HexColor("#DDDDDD")

def add_watermark(canvas, doc, bill):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 40)
    canvas.setFillGray(0.92)
    canvas.translate(300, 420)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, bill.payment_status.upper())
    canvas.restoreState()

def generate_invoice_pdf(bill, business):
    output_dir = Path(settings.MEDIA_ROOT) / "invoices"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{bill.bill_number.replace('/', '_')}.pdf"

    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleStyle", fontSize=18, textColor=NAVY, spaceAfter=12, leading=22))
    styles.add(ParagraphStyle(name="Label", fontSize=10, textColor=black, leading=14))
    styles.add(ParagraphStyle(name="Footer", fontSize=9, textColor=HexColor("#555555"), alignment=1))

    elements = []

    left_logo = ""
    if business.logo and os.path.exists(business.logo.path):
        left_logo = Image(business.logo.path, width=48, height=48)

    right_logo_path = os.path.join(settings.BASE_DIR, "static", "bizsight_logo.png")
    right_logo = Image(right_logo_path, width=48, height=48) if os.path.exists(right_logo_path) else Paragraph("BizSight", styles["TitleStyle"])

    logo_table = Table([[left_logo, right_logo]], colWidths=[240, 240])
    logo_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(logo_table)
    elements.append(Spacer(1, 12))

    party_table = Table([[
        Paragraph(
            f"<b>Seller</b><br/>{business.name}<br/>{business.address or ''}"
            f"<br/>Phone: {business.phone or '-'}<br/>Email: {business.email or '-'}",
            styles["Label"]
        ),
        Paragraph(
            f"<b>Bill To</b><br/>{bill.customer_name or 'Walk-in Customer'}"
            f"<br/>{bill.customer_address or ''}<br/>Phone: {bill.customer_phone or '-'}",
            styles["Label"]
        )
    ]], colWidths=[85 * mm, 85 * mm])
    party_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, NAVY),
        ("BACKGROUND", (0, 0), (-1, -1), IVORY),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(party_table)
    elements.append(Spacer(1, 16))

    item_data = [["Item", "Qty", "Price", "Amount"]]
    for item in bill.items.all():
        item_data.append([
            item.item_name,
            item.quantity,
            f"{item.price}",
            f"{item.total}",
        ])
    item_table = Table(item_data, colWidths=[80 * mm, 25 * mm, 35 * mm, 35 * mm])
    item_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.25, black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    elements.append(item_table)
    elements.append(Spacer(1, 12))

    totals_table = Table([
        ["Subtotal", f"{bill.subtotal}"],
        ["Discount", f"{bill.discount}"],
        ["Total Amount", f"{bill.total_amount}"],
    ], colWidths=[120 * mm, 35 * mm])
    totals_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("BACKGROUND", (0, -1), (-1, -1), NAVY),
        ("TEXTCOLOR", (0, -1), (-1, -1), white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("This is a computer-generated bill. No signature required.", styles["Footer"])
    )

    doc.build(
    elements,
    onFirstPage=lambda canvas, doc: add_watermark(canvas, doc, bill),
    onLaterPages=lambda canvas, doc: add_watermark(canvas, doc, bill)
)


    return str(file_path)