from django.db import models
from accounts.models import Business
from django.utils import timezone

from django.db import models
from django.utils import timezone
from accounts.models import Business


class Bill(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid'),
        ('PAY_LATER', 'Pay Later'),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='bills'
    )

    bill_number = models.CharField(max_length=50, unique=True, blank=True)

    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)

    customer_email = models.EmailField(blank=True, null=True)

    customer_address = models.TextField(blank=True, null=True)

    email_required = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PAID'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto bill number
        if not self.bill_number:
            year = timezone.now().year
            count = Bill.objects.filter(
                business=self.business,
                created_at__year=year
            ).count() + 1
            self.bill_number = f"BS/{year}/{count:06d}"

        # Total safety
        calculated_total = self.subtotal - self.discount
        if calculated_total < 0:
            calculated_total = 0
        self.total_amount = calculated_total

        # ₹5,000 email rule
        self.email_required = self.total_amount >= 5000

        super().save(*args, **kwargs)

    def get_upi_payment_uri(self, upi_id: str, payee_name: str):
        from urllib.parse import quote

        amount = str(self.total_amount)
        note = quote(self.bill_number)
        payee = quote(payee_name)

        return (
            f"upi://pay?"
            f"pa={upi_id}"
            f"&pn={payee}"
            f"&am={amount}"
            f"&tn={note}"
        )

class BillItem(models.Model):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='items'
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
