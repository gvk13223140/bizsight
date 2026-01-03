# BizSight & BizMitra

BizSight is a Django-based business intelligence and billing platform designed for small and medium businesses.  
BizMitra is the AI-powered companion layer that adds insights, alerts, and risk intelligence on top of BizSight’s data.

Together, they help business owners **manage billing, analyze sales, and understand business risks** from a single system.

---

## Why BizSight?

Many small businesses still rely on:
- Manual billing
- Basic spreadsheets
- No real analytics
- No visibility into risks or trends

BizSight was built to solve this gap with a **simple, practical, and extensible system** that focuses on:
- Day-to-day billing
- Clear sales analytics
- Easy data imports
- Actionable insights

No heavy ERP. No unnecessary complexity.

---

## What is BizMitra?

BizMitra is the **intelligence layer** of BizSight.

It works as a digital business companion that:
- Analyzes billing and sales data
- Generates smart insights
- Raises alerts for risky patterns
- Uses a trained ML model for risk scoring
- Provides a guided, chat-style experience

BizMitra does not replace business owners — it **assists decision-making**.

---

## Core Features

### Billing
- Create bills with multiple items
- Track paid, unpaid, and pay-later bills
- Automatic bill numbering
- Soft delete support
- PDF invoice generation
- Optional email delivery of invoices

---

### UPI Payments
- Business can add its own UPI ID
- QR code generated per bill
- If UPI is not configured, the system prompts the business to add it
- Works seamlessly for walk-in and registered customers

---

### Analytics Dashboard
- Daily and monthly sales trends
- Total sales, bill count, paid/unpaid metrics
- Top-selling items
- Visual charts using real business data
- Date-range filtering

---

### Data Import
- Import bills directly from:
  - Google Sheets (public CSV export)
  - CSV file uploads
- Preview data before import
- Handles real-world cases like:
  - Missing emails
  - Walk-in customers
  - Mixed payment modes
- Includes a ready-to-use CSV template

---

### Exports
- Download sales data as:
  - CSV
  - Excel
  - PDF reports
- Date-filtered exports supported



### BizMitra Intelligence
- Smart insights based on sales behavior
- Alerts for unusual or risky patterns
- Risk prediction using a trained TensorFlow model
- Modular AI services (alerts, insights, chat, feature extraction)


## Tech Stack

- **Backend**: Django
- **Database**: SQLite (development)
- **Frontend**: Django Templates + CSS
- **Analytics**: Custom aggregation services
- **AI / ML**:
  - TensorFlow (pre-trained model)
  - Scikit-learn (scaler)
- **Charts**: Chart.js
- **Imports**: Google Sheets CSV + file uploads


## Project Structure

core/ → Django project settings
accounts/ → Authentication & business profiles
billing/ → Billing, invoices, analytics
analytics_engine/ → Sales metrics & insights
bizmitra/ → AI companion (alerts, chat, risk model)
insights/ → Business insight services
static/ → Images & templates


---

## ML & Risk Model

- `risk_model.h5` is a **pre-trained TensorFlow model**
- `scaler.pkl` is used for feature scaling
- Models are **loaded at runtime**
- Training logic exists but is not executed in production
- Inference behavior remains unchanged

---

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/gvk13223140/bizsight.git
cd bizsight

Create Virtual Environment
python -m venv venv
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Environment Variables

Create a .env file (not committed to GitHub):

DJANGO_SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

Run Migrations
python manage.py migrate

Start Server
python manage.py runserver


Open: http://127.0.0.1:8000
