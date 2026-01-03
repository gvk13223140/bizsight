import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from billing.models import Bill, BillItem
from accounts.models import Business


class Command(BaseCommand):
    help = "Seed 6 months of demo billing data for all businesses"

    def handle(self, *args, **kwargs):
        BILLS_PER_BUSINESS = 250
        MONTHS_BACK = 6

        ITEM_CATALOG = [
            ("Rice Bag", 50, 1200),
            ("Cooking Oil", 1, 900),
            ("Milk Packet", 1, 60),
            ("Sugar", 1, 45),
            ("Notebook", 1, 80),
            ("Pen", 1, 20),
            ("Mobile Charger", 1, 650),
            ("Headphones", 1, 1200),
            ("Tablet Strip", 1, 140),
            ("Soap", 1, 35),
        ]

        PAYMENT_STATUSES = (
            ["PAID"] * 70 +
            ["UNPAID"] * 20 +
            ["PAY_LATER"] * 10
        )

        def random_date_within_months(months):
            now = timezone.now()
            start = now - timedelta(days=months * 30)
            return start + timedelta(
                seconds=random.randint(0, int((now - start).total_seconds()))
            )

        businesses = Business.objects.all()
        if not businesses.exists():
            self.stdout.write(self.style.ERROR("❌ No businesses found"))
            return

        for business in businesses:
            self.stdout.write(f"🚀 Seeding data for {business.name}")

            for _ in range(BILLS_PER_BUSINESS):
                bill_date = random_date_within_months(MONTHS_BACK)

                num_items = random.randint(1, 5)
                selected_items = random.sample(ITEM_CATALOG, num_items)

                subtotal = 0
                items = []

                for name, min_qty, max_price in selected_items:
                    qty = random.randint(1, 3)
                    price = random.randint(min_qty * 10, max_price)
                    total = qty * price
                    subtotal += total

                    items.append((name, qty, price, total))

                discount = random.choice([0, 0, 0, 50, 100, 200])
                payment_status = random.choice(PAYMENT_STATUSES)

                year = bill_date.year
                existing_count = Bill.objects.filter(
                    business=business,
                    created_at__year=year
                ).count() + 1

                bill_number = f"BS/{year}/{existing_count:06d}"

                bill = Bill.objects.create(
                    business=business,
                    bill_number=bill_number,
                    customer_name=random.choice(
                        ["Walk-in", "Regular Customer", "Wholesale Buyer", None]
                    ),
                    subtotal=subtotal,
                    discount=discount,
                    payment_status=payment_status,
                )

                # force realistic created_at
                Bill.objects.filter(id=bill.id).update(created_at=bill_date)


                # force realistic created_at
                Bill.objects.filter(id=bill.id).update(created_at=bill_date)

                for name, qty, price, total in items:
                    BillItem.objects.create(
                        bill=bill,
                        item_name=name,
                        quantity=qty,
                        price=price,
                        total=total,
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"{BILLS_PER_BUSINESS} bills created for {business.name}"
                )
            )

        self.stdout.write(self.style.SUCCESS("🎉 ALL DATA SEEDED SUCCESSFULLY"))
