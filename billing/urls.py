from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("create/", create_bill_view, name="create_bill"),
    path("bill/<int:bill_id>/", bill_detail_view, name="bill_detail"),
    path("bill/<int:bill_id>/download/", download_bill_pdf, name="download_bill_pdf"),
    path("test-ui/", test_ui),
    path("bills/", bills_list_view, name="bills_list"),
    path("analytics/", analytics_dashboard_view, name="analytics"),
    path("import/google-sheet/",import_google_sheet_view,name="import_google_sheet"),
    path("reports/sales/csv/", download_sales_csv, name="download_sales_csv"),
    path("reports/sales/excel/", download_sales_excel, name="download_sales_excel"),
    path("reports/sales/pdf/", download_sales_pdf, name="download_sales_pdf"),
]