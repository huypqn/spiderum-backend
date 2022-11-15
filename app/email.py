from mailjet_rest import Client
from app import app
from app.services import get_register_token

def send_register_email(email):
    token = f"{app.config['WEBSITE_URI']}/tao-tai-khoan?token={get_register_token(email)}"
    mailjet = Client(
        auth=(app.config['API_KEY'], app.config['API_SECRET']),
        version='v3.1'
    )
    
    data = {
        "Messages": [
            {
                "From": {
                    "Email": app.config['NOREPLY'],
                    "Name": "Spider"
                },
                "To": [
                    {
                        "Email": email,
                    }
                ],
                "TemplateID": 4348146,
                "TemplateLanguage": True,
                "Subject": "Xác nhận địa chỉ email cho tài khoản của bạn",
                "Variables": {
                    "token": token
                }
            },
        ]
    }
    result = mailjet.send.create(data=data)
    return result