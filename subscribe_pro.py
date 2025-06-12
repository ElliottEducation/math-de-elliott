import stripe
import os
from dotenv import load_dotenv

load_dotenv()

# Load Stripe secret key from .env
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Define price IDs for monthly and yearly subscriptions
MONTHLY_PRICE_ID = os.getenv("STRIPE_MONTHLY_PRICE_ID")
YEARLY_PRICE_ID = os.getenv("STRIPE_YEARLY_PRICE_ID")

# Define your site domain
DOMAIN = os.getenv("DOMAIN", "http://localhost:8501")

def create_checkout_session(mode="monthly"):
    try:
        price_id = MONTHLY_PRICE_ID if mode == "monthly" else YEARLY_PRICE_ID

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=f"{DOMAIN}?success=true",
            cancel_url=f"{DOMAIN}?canceled=true",
        )
        return session.url
    except Exception as e:
        print(f"Error creating Stripe checkout session: {e}")
        return None
