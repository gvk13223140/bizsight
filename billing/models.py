import uuid
from django.db import models
from django.utils import timezone
from accounts.models import Business 

class Bill(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("PAID", "Paid"),
        ("UNPAID", "Unpaid"),
        ("PAY_LATER", "Pay Later"),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="bills",
    )

    bill_number = models.CharField(max_length=100, blank=True)

    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PAID",
    )

    email_required = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)

    class Meta:
        unique_together = ("business", "bill_number")
        ordering = ["-created_at"]



    def save(self, *args, **kwargs):
        if not self.bill_number:
            year = timezone.now().year
            business_name = self.business.name.replace(" ", "").upper()
            self.bill_number = f"BS_{year}_{business_name}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)



    def get_upi_payment_uri(self, upi_id: str, payee_name: str):
        from urllib.parse import quote

        return (
            f"upi://pay?"
            f"pa={upi_id}"
            f"&pn={quote(payee_name)}"
            f"&am={self.total_amount}"
            f"&tn={quote(self.bill_number)}"
        )



class BillItem(models.Model):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name="items",
    )

    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item_name} ({self.bill.bill_number})"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI'),
        ('CASH', 'Cash'),
    ]

    bill = models.OneToOneField(
        Bill,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES
    )

    reference_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bill.bill_number} - {self.method}"
