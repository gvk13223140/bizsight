from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import date
import os
from analytics_engine.services.sales_metrics import get_sales_overview
from analytics_engine.services.item_metrics import get_top_items
from analytics_engine.services.smart_insights import get_smart_insights
from .models import Bill, BillItem
from .utils import generate_upi_qr
from .invoice_pdf import generate_invoice_pdf
from insights.services import get_bizmitra_insights
from accounts.models import Business
from django.http import FileResponse
import csv
from django.http import HttpResponse
from datetime import timedelta


def test_ui(request):
    return render(request, "billing/test_ui.html")


def dashboard_view(request):
    today = date.today()

    bills_today = Bill.objects.filter(created_at__date=today)

    metrics = {
        "today_sales": bills_today.filter(
            payment_status="PAID"
        ).aggregate(total=Sum("total_amount"))["total"] or 0,

        "total_bills": Bill.objects.count(),
        "paid": Bill.objects.filter(payment_status="PAID").count(),
        "unpaid": Bill.objects.filter(payment_status="UNPAID").count(),
        "pay_later": Bill.objects.filter(payment_status="PAY_LATER").count(),
    }

    recent_bills = Bill.objects.order_by("-created_at")[:5]

    context = {
        "today": timezone.now().strftime("%A, %d %B %Y"),
        "metrics": metrics,
        "recent_bills": recent_bills,
    }

    return render(request, "billing/dashboard.html", context)


def create_bill_view(request):
    if request.method == "POST":
        print("🔥 CREATE BILL POST HIT 🔥")

        from accounts.utils import get_current_business

    business = get_current_business(request)
    if not business:
        messages.error(request, "Please login to continue")
        return redirect("login")

        customer_name = request.POST.get("customer_name", "").strip()
        customer_phone = request.POST.get("customer_phone", "").strip()
        customer_email = request.POST.get("customer_email", "").strip()
        customer_address = request.POST.get("customer_address", "").strip()

        payment_status = request.POST.get("payment_status")
        discount = float(request.POST.get("discount") or 0)

        item_names = request.POST.getlist("item_name[]")
        quantities = request.POST.getlist("quantity[]")
        prices = request.POST.getlist("price[]")

        subtotal = 0
        items_data = []

        for name, qty, price in zip(item_names, quantities, prices):
            name = name.strip()
            qty = int(qty or 0)
            price = float(price or 0)

            if not name or qty <= 0 or price <= 0:
                continue

            total = qty * price
            subtotal += total

            items_data.append({
                "name": name,
                "qty": qty,
                "price": price,
                "total": total
            })

        if not items_data:
            messages.error(request, "Please add at least one valid item.")
            return redirect("create_bill")

        if subtotal - discount >= 5000 and not customer_email:
            messages.error(request, "Email is required for bills above ₹5000")
            return redirect("create_bill")

        bill = Bill.objects.create(
            business=business,
            customer_name=customer_name or None,
            customer_phone=customer_phone or None,
            customer_email=customer_email or None,
            customer_address=customer_address or None,
            subtotal=subtotal,
            discount=discount,
            payment_status=payment_status
        )

        for item in items_data:
            BillItem.objects.create(
                bill=bill,
                item_name=item["name"],
                quantity=item["qty"],
                price=item["price"],
                total=item["total"]
            )

        print("✅ REDIRECTING TO BILL:", bill.id)
        return redirect("bill_detail", bill_id=bill.id)

    return render(request, "billing/create_bill.html")



def bill_detail_view(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    business = bill.business

    bizmitra_insights = get_bizmitra_insights(business)

    upi_uri = bill.get_upi_payment_uri(
        upi_id="vamshi7@ptyes",
        payee_name=business.name
    )

    qr_path = generate_upi_qr(
        upi_uri=upi_uri,
        bill_number=bill.bill_number
    )

    qr_url = settings.MEDIA_URL + qr_path.replace("\\", "/").split("media/")[-1]

    context = {
        "bill": bill,
        "business": business,
        "qr_url": qr_url,
        "bizmitra_insights": bizmitra_insights,
    }

    return render(request, "billing/bill_detail.html", context)


def download_bill_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    business = bill.business

    pdf_path = generate_invoice_pdf(bill=bill, business=business)

    from django.utils.encoding import smart_str

    response = FileResponse(open(pdf_path, "rb"), as_attachment=True)
    response["Content-Disposition"] = (
        f'attachment; filename="{smart_str(os.path.basename(pdf_path))}"'
    )

    return response
def bills_list_view(request):
    bills = Bill.objects.select_related("business").order_by("-created_at")

    for bill in bills:
        bill.status_label = bill.payment_status.replace("_", " ").title()

    return render(
        request,
        "billing/bills_list.html",
        {"bills": bills}
    )
from analytics_engine.services.sales_metrics import get_sales_overview, get_sales_by_day
from analytics_engine.services.item_metrics import get_top_items
from analytics_engine.services.smart_insights import get_smart_insights


import json

def analytics_dashboard_view(request):
    from accounts.utils import get_current_business

    business = get_current_business(request)
    if not business:
        messages.error(request, "Please login to continue")
        return redirect("login")

    overview = get_sales_overview(business)
    sales_trend = get_sales_by_day(business, days=7)
    top_items = get_top_items(business)
    insights = get_smart_insights(business)

    labels = [str(row["created_at__date"]) for row in sales_trend]
    values = [float(row["total"]) for row in sales_trend]

    context = {
        "overview": overview,
        "top_items": top_items,
        "insights": insights,
        "chart_labels": json.dumps(labels),
        "chart_values": json.dumps(values),
    }

    return render(request, "billing/analytics.html", context)
import requests
import csv
from io import StringIO
from django.contrib import messages
from django.shortcuts import redirect
from datetime import datetime

def extract_sheet_csv_url(sheet_url):
    sheet_id = sheet_url.split("/d/")[1].split("/")[0]
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
def import_google_sheet_view(request):
    if request.method != "POST":
        return redirect("analytics")

    sheet_url = request.POST.get("sheet_url")
    from accounts.utils import get_current_business

    business = get_current_business(request)
    if not business:
        messages.error(request, "Please login to continue")
        return redirect("login")

    try:
        csv_url = extract_sheet_csv_url(sheet_url)
        response = requests.get(csv_url)
        response.raise_for_status()
    except Exception:
        messages.error(request, "Invalid or private Google Sheet")
        return redirect("analytics")

    csv_data = StringIO(response.text)
    reader = csv.DictReader(csv_data)

    bills_created = 0

    for row in reader:
        try:
            qty = int(row["quantity"])
            price = float(row["price"])
            total = qty * price

            bill = Bill.objects.create(
                business=business,
                customer_name="Imported (Google Sheet)",
                subtotal=total,
                discount=0,
                payment_status="PAID"
            )

            BillItem.objects.create(
                bill=bill,
                item_name=row["item_name"],
                quantity=qty,
                price=price,
                total=total
            )

            bills_created += 1

        except Exception:
            continue

    messages.success(
        request,
        f"Imported {bills_created} rows successfully"
    )

    return redirect("analytics")
def download_sales_csv(request):
    from accounts.utils import get_current_business

    business = get_current_business(request)
    if not business:
        messages.error(request, "Please login to continue")
        return redirect("login")
    if not business:
        messages.error(request, "Business not configured yet.")
        return redirect("dashboard")
    last_7_days = timezone.now() - timedelta(days=7)

    bills = Bill.objects.filter(
        business=business,
        created_at__gte=last_7_days
    )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="sales_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Bill Number", "Date", "Customer",
        "Subtotal", "Discount", "Total", "Status"
    ])

    for bill in bills:
        writer.writerow([
            bill.bill_number,
            bill.created_at.date(),
            bill.customer_name or "-",
            bill.subtotal,
            bill.discount,
            bill.total_amount,
            bill.payment_status
        ])

    return response
from openpyxl import Workbook
def download_sales_excel(request):
    from accounts.utils import get_current_business

    business = get_current_business(request)
    if not business:
        messages.error(request, "Please login to continue")
        return redirect("login")
    if not business:
        messages.error(request, "Business not configured yet.")
        return redirect("dashboard")

    last_7_days = timezone.now() - timedelta(days=7)

    bills = Bill.objects.filter(
        business=business,
        created_at__gte=last_7_days
    )

    wb = Workbook()
    ws = wb.active
    ws.title = "Sales Report"

    ws.append([
        "Bill Number", "Date", "Customer",
        "Subtotal", "Discount", "Total", "Status"
    ])

    for bill in bills:
        ws.append([
            bill.bill_number,
            bill.created_at.strftime("%Y-%m-%d"),
            bill.customer_name or "-",
            float(bill.subtotal),
            float(bill.discount),
            float(bill.total_amount),
            bill.payment_status
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="sales_report.xlsx"'

    wb.save(response)
    return response
def dev_login(request):
    business = Business.objects.first()
    request.session["business_id"] = business.id
    return redirect("dashboard")

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
def download_sales_pdf(request):
    from accounts.utils import get_current_business

    business = get_current_business(request)
    if not business:
        messages.error(request, "Please login to continue")
        return redirect("login")

    if not business:
        messages.error(request, "No business found. Please set up your business profile.")
        return redirect("dashboard")

    last_7_days = timezone.now() - timedelta(days=7)

    bills = Bill.objects.filter(
        business=business,
        created_at__gte=last_7_days
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="sales_summary.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []
    business_name = business.name if business else "BizSight"
    elements.append(Paragraph(
    f"<b>BizSight Sales Report</b><br/>{business_name}",
    styles["Title"]
))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Bill", "Date", "Customer", "Total", "Status"]
    ]

    for bill in bills:
        table_data.append([
            bill.bill_number,
            bill.created_at.strftime("%d-%m-%Y"),
            bill.customer_name or "-",
            f"₹{bill.total_amount}",
            bill.payment_status
        ])

    table = Table(table_data)
    elements.append(table)

    doc.build(elements)
    return response
