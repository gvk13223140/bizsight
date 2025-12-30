from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black
from reportlab.lib.units import mm
from pathlib import Path


NAVY = HexColor("#0A1F44")
IVORY = HexColor("#F9F6F1")


def generate_invoice_pdf(bill, business):
    output_dir = Path("media/invoices")
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
    styles.add(ParagraphStyle(
        name="TitleStyle",
        fontSize=18,
        textColor=NAVY,
        spaceAfter=12,
        leading=22,
    ))

    styles.add(ParagraphStyle(
        name="Label",
        fontSize=10,
        textColor=black,
        leading=14,
    ))

    elements = []

    # ---------- HEADER ----------
    elements.append(Paragraph("BILL", styles["TitleStyle"]))

    header_table = Table(
        [
            ["Bill No:", bill.bill_number, "Date:", bill.created_at.date()],
            ["Payment Status:", bill.payment_status, "", ""],
        ],
        colWidths=[30*mm, 60*mm, 30*mm, 40*mm]
    )

    header_table.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # ---------- SELLER / CUSTOMER ----------
    party_table = Table(
        [
            [
                Paragraph("<b>Seller</b><br/>" +
                          f"{business.name}<br/>{business.address}<br/>"
                          f"Phone: {business.phone}<br/>Email: {business.email}",
                          styles["Label"]),
                Paragraph("<b>Bill To</b><br/>" +
                          f"{bill.customer_name or 'Walk-in Customer'}<br/>"
                          f"{bill.customer_address or ''}<br/>"
                          f"Phone: {bill.customer_phone or '-'}",
                          styles["Label"])
            ]
        ],
        colWidths=[85*mm, 85*mm]
    )

    party_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, black),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(party_table)
    elements.append(Spacer(1, 16))

    # ---------- ITEMS TABLE ----------
    table_data = [
        ["Item", "Qty", "Price", "Amount"]
    ]

    for item in bill.items.all():
        table_data.append([
            item.item_name,
            str(item.quantity),
            f"{item.price}",
            f"{item.total}",
        ])

    item_table = Table(
        table_data,
        colWidths=[80*mm, 25*mm, 35*mm, 35*mm]
    )

    item_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, black),
        ("BACKGROUND", (0, 0), (-1, 0), IVORY),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(item_table)
    elements.append(Spacer(1, 12))

    # ---------- TOTALS ----------
    totals_table = Table(
        [
            ["Subtotal", f"{bill.subtotal}"],
            ["Discount", f"{bill.discount}"],
            ["Total Amount", f"{bill.total_amount}"],
        ],
        colWidths=[120*mm, 35*mm]
    )

    totals_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("FONT", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (0, -1), (-1, -1), 1, black),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(totals_table)
    elements.append(Spacer(1, 20))
    elements.append(Spacer(1, 8))

    totals_table = Table(
        [
            ["Subtotal", str(bill.subtotal)],
            ["Discount", str(bill.discount)],
            ["Total Amount", str(bill.total_amount)],
        ],
        colWidths=[350, 90]
    )

    totals_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (0, -1), (-1, -1), 1.5, colors.black),
        ("TOPPADDING", (0, -1), (-1, -1), 8),
    ]))

    elements.append(totals_table)

    # ---------- FOOTER ----------
    elements.append(
        Paragraph(
            "This is a computer-generated bill. No signature required.",
            styles["Italic"]
        )
    )


    doc.build(elements)

    return str(file_path)