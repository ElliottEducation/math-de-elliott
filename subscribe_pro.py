import stripe
import os
from dotenv import load_dotenv
from supabase import create_client

# 加载环境变量
load_dotenv()

# 初始化 Stripe 和 Supabase
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 获取 Price ID 与返回网址
MONTHLY_PRICE_ID = os.getenv("STRIPE_MONTHLY_PRICE_ID")
YEARLY_PRICE_ID = os.getenv("STRIPE_YEARLY_PRICE_ID")
DOMAIN_URL = os.getenv("DOMAIN_URL").rstrip("/")


# 创建 Stripe Checkout 会话
def create_checkout_session(email, billing_period="monthly"):
    try:
        price_id = MONTHLY_PRICE_ID if billing_period == "monthly" else YEARLY_PRICE_ID

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{DOMAIN_URL}/?success=true&email={email}",
            cancel_url=f"{DOMAIN_URL}/?canceled=true",
        )

        return session.url

    except Exception as e:
        print("❌ Stripe Checkout Error:", str(e))
        return None


# 支付成功后：更新 Supabase 中的用户身份
def upgrade_user_role(email):
    try:
        response = supabase.table("users").update({"user_role": "pro"}).eq("email", email).execute()
        print(f"✅ User {email} upgraded to Pro")
        return True
    except Exception as e:
        print("❌ Failed to update user role:", str(e))
        return False
