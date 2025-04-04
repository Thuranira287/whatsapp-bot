from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    msg = response.message()

    if 'hi' in incoming_msg:
        msg.body("Hello! I'm your bot. How can I assist you today?")
    elif 'help' in incoming_msg:
        msg.body("Type:\n- 'hi' to greet\n- 'info' for more info")
    elif 'info' in incoming_msg:
        msg.body("This is a test WhatsApp bot powered by Twilio and Flask.")
    else:
        msg.body("Sorry, I didn't get that. Type 'help' for options.")

    return str(response)

if __name__ == '__main__':
    app.run()
