import stripe
import os
from dotenv import load_dotenv

load_dotenv()

# 设置 Stripe 密钥
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# 从环境变量中读取 Price ID
MONTHLY_PRICE_ID = os.getenv("STRIPE_MONTHLY_PRICE_ID")
YEARLY_PRICE_ID = os.getenv("STRIPE_YEARLY_PRICE_ID")

def create_checkout_session(plan="monthly"):
    try:
        domain_url = os.getenv("DOMAIN_URL").rstrip("/")

        # 根据传入的 plan 参数选择价格 ID
        price_id = MONTHLY_PRICE_ID if plan == "monthly" else YEARLY_PRICE_ID

        # 创建 Stripe Checkout 会话
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
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
