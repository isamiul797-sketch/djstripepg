DJ-Stripe Payment Gateway Backend

Project Overview

This is a Django backend project built for handling Stripe payments and webhooks, designed to work without any frontend templates.
All responses are in JSON, making it ideal for mobile apps, REST clients, or Single Page Applications (SPA).

Main Features:

Create Stripe Checkout Sessions for products

Receive and verify Stripe Webhook events

Automatically update order status on successful payment

JSON-only responses (no HTML templates)

CSRF-safe webhook endpoints

Installation

1.Clone the repository
https://github.com/isamiul797-sketch/djstripepg

cd djstripepg

2.Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

3.Install dependencies
pip install -r requirements.txt

4.Set up environment variables
Create a .env file in the project root:
SECRET_KEY=<your-django-secret-key>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_NAME=db.sqlite3
STRIPE_SECRET_KEY=<your-stripe-secret-key>
STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>
STRIPE_WEBHOOK_SECRET=<your-stripe-webhook-secret>
CSRF_TRUSTED_ORIGINS=https://<ngrok-or-domain>

5.Run migrations
python manage.py migrate

Start Django Server
python manage.py runserver

Stripe Checkout

Endpoint: /create_payment/<product_id>/

Method: POST

Response: Redirects to Stripe Checkout session URL


Stripe Webhook

Endpoint: /stripe_webhook/

Method: POST

CSRF: Exempt, verifies Stripe signature

Notes

Backend-only project: No HTML templates required.

All responses are JSON or redirect to Stripe checkout.

Make sure STRIPE_WEBHOOK_SECRET is set correctly.

Update CSRF trusted origins if using ngrok or custom domains.

Use ngrok to expose local server for Stripe webhooks during development.
