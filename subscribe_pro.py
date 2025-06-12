# subscribe_pro.py

import os
import stripe
from dotenv import load_dotenv

# ✅ 加载 .env 文件中的环境变量
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# ✅ 从 .env 读取 Price ID
MONTHLY_PRICE_ID = os.getenv("STRIPE_MONTHLY_PRICE_ID")
YEARLY_PRICE_ID = os.getenv("STRIPE_YEARLY_PRICE_ID")

# ✅ 封装 Checkout Session 创建函数
def create_checkout_session(user_email: str, plan: str = "monthly") -> str:
    """
    创建一个 Stripe Checkout 订阅会话，返回支付链接 URL。
    参数:
        user_email: 登录用户的邮箱
        plan: "monthly" 或 "yearly"
    返回:
        checkout_url: 支付页面链接
    """
    try:
        if plan == "yearly":
            price_id = YEARLY_PRICE_ID
        else:
            price_id = MONTHLY_PRICE_ID

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            customer_email=user_email,
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            success_url="https://math-de-elliott.streamlit.app/?payment=success",
            cancel_url="https://math-de-elliott.streamlit.app/?payment=cancelled",
        )
        return checkout_session.url

    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return ""
