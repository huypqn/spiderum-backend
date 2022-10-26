from app import app

@app.route('/v1/api/<token>')
def auth(token):
    ...

@app.route('/v1/api/user')
def getUser():
    user = [
        {
            "username": "haohmaru25",
            "email": "haohmaru@example.com"
        },
        {
            "username": "abc25",
            "email": "abc@example.com"
        }
    ]
    return user