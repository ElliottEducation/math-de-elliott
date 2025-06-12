import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
MONTHLY_PRICE_ID = os.getenv("STRIPE_MONTHLY_PRICE_ID")
YEARLY_PRICE_ID = os.getenv("STRIPE_YEARLY_PRICE_ID")

def create_checkout_session(email, billing_period="monthly"):
    try:
        domain_url = os.getenv("DOMAIN_URL").rstrip("/")
        price_id = MONTHLY_PRICE_ID if billing_period == "monthly" else YEARLY_PRICE_ID

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=email,  # ⭐ 将用户邮箱用于 Stripe 账户识别
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=domain_url + "/?success=true",
            cancel_url=domain_url + "/?canceled=true",
        )

        return checkout_session.url

    except Exception as e:
        print("❌ Stripe Checkout Error:", str(e))
        return None
