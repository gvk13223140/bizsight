from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),

    path("create/", views.create_bill_view, name="create_bill"),
    path("bill/<int:bill_id>/", views.bill_detail_view, name="bill_detail"),
    path("bill/<int:bill_id>/download/", views.download_bill_pdf, name="download_bill_pdf"),
    path("bill/<int:bill_id>/delete/", views.delete_bill_view, name="delete_bill"),
    path("bill/<int:bill_id>/mark-paid/", views.mark_bill_paid, name="mark_bill_paid"),

    path("bills/", views.bills_list_view, name="bills_list"),
    path("bills/bulk-delete/", views.bulk_delete_bills_view, name="bulk_delete_bills"),

    path("analytics/", views.analytics_dashboard_view, name="analytics"),

    path("import/google-sheet/", views.import_google_sheet_view, name="import_google_sheet"),
    path("import-csv/", views.import_csv_file_view, name="import_csv_file"),

    path("download/csv/", views.download_sales_csv, name="download_sales_csv"),
    path("download/excel/", views.download_sales_excel, name="download_sales_excel"),
    path("download/pdf/", views.download_sales_pdf, name="download_sales_pdf"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
