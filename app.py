from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import datetime
import openai  # Step 3 prep

app = Flask(__name__)

# OpenAI setup (Step 3 - add your API key here)
openai.api_key = 'your-openai-api-key'

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def log_message(sender, message):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)',
              (sender, message, str(datetime.datetime.now())))
    conn.commit()
    conn.close()

@app.route('/whatsapp', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    sender = request.values.get('From')
    response = MessagingResponse()
    msg = response.message()

    log_message(sender, incoming_msg)

    # Step 3: Respond with GPT if keyword 'ai' is used
    if 'ai' in incoming_msg:
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        msg.body(reply['choices'][0]['message']['content'])

    # Step 4: Send image or PDF
    elif 'image' in incoming_msg:
        msg.body("Here's an image for you:")
        msg.media("https://www.example.com/image.jpg")  # Replace with your image URL
    elif 'pdf' in incoming_msg:
        msg.body("Here's your PDF:")
        msg.media("https://www.example.com/file.pdf")  # Replace with your file URL

    # Regular logic
    elif 'hi' in incoming_msg:
        msg.body("Hello! I'm your smart WhatsApp bot. Ask me anything or say 'ai [your question]'!")
    elif 'help' in incoming_msg:
        msg.body("Type:\n- 'hi' to greet\n- 'ai [question]' to talk with ChatGPT\n- 'image' or 'pdf' to get media.")
    else:
        msg.body("Sorry, I didn't get that. Type 'help' for options.")

    return str(response)

if __name__ == '__main__':
    app.run()
