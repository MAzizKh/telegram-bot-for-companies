from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
user_state = {}

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if chat_id not in user_state:
            user_state[chat_id] = {"step": "start"}

        state = user_state[chat_id]

        if text == "/start":
            send_message(chat_id, "🍰 Assalomu alaykum! Qanday tort buyurtma qilasiz?")
            send_buttons(chat_id, ["🍫 Shokoladli", "🍓 Mevali", "🍮 Cheesecake"])
            state["step"] = "cake"

        elif state["step"] == "cake":
            state["cake"] = text
            send_message(chat_id, "📦 Nechta dona kerak?")
            state["step"] = "quantity"

        elif state["step"] == "quantity":
            state["quantity"] = text
            send_message(chat_id, "🕐 Yetkazish vaqtini kiriting (masalan: 6 iyul, 18:00)")
            state["step"] = "time"

        elif state["step"] == "time":
            state["time"] = text
            send_message(chat_id, "📞 Telefon raqamingizni kiriting:")
            state["step"] = "phone"

        elif state["step"] == "phone":
            state["phone"] = text
            send_message(chat_id, "💳 To'lov uchun havola: https://your-click-link.uz")
            send_message(chat_id, "✅ To'lov qilgandan so'ng 'To'lov qildim' deb yozing.")
            state["step"] = "payment"

        elif state["step"] == "payment" and "to'lov qildim" in text.lower():
            send_message(chat_id, "🎉 Rahmat! Buyurtmangiz qabul qilindi.")
            print("✅ Yangi buyurtma:", state)
            state["step"] = "done"

        else:
            send_message(chat_id, "Iltimos, /start deb yozing va ko‘rsatmalarga amal qiling.")
    return "ok"

def send_message(chat_id, text):
    requests.post(API_URL, json={"chat_id": chat_id, "text": text})

def send_buttons(chat_id, buttons):
    kb = {"keyboard": [[{"text": b}] for b in buttons], "resize_keyboard": True}
    requests.post(API_URL, json={"chat_id": chat_id, "text": "Tanlang:", "reply_markup": kb})

if __name__ == "__main__":
    app.run()