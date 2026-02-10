from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from dotenv import load_dotenv
import resend
import os
import traceback

load_dotenv()
app = Flask(__name__)
api = Api(app)
CORS(app)

API_KEY = os.getenv("API_KEY")

email_args = reqparse.RequestParser()
email_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
email_args.add_argument('subject', type=str, required=True, help="Subject cannot be blank")
email_args.add_argument('message', type=str, required=True, help="Message cannot be blank")

resend.api_key = os.getenv("RESEND_API_KEY")

class Email(Resource):
    def post(self):
        client_key = request.headers.get("X-API-KEY")

        if client_key != API_KEY:
            return {"error": "Unauthorized"}, 401

        args = email_args.parse_args()
        link = os.getenv('PORTFOLIO_LINK')
        try:

            params = {
                "from": os.getenv('MAIL_EMAIL'),
                "to": [args["email"]],
                "subject": args["subject"],
                "html": f"""
                         <p>{args["message"]}</p><br><br>
                         <p><strong>Thank you for connecting with me.</strong></p><br>
                         <p>Here is the link to my portfolio website: <br>
                         <a href="{link}">{link}</a></p>
                        """
            }

            r = resend.Emails.send(params)

            return {"message": "Email sent successfully!"}, 201
        except Exception as e:
            print("Email sending error:", e)
            traceback.print_exc()
            return {"error": str(e)}, 500

api.add_resource(Email, '/api/email/')

if __name__ == '__main__':
    app.run(debug=False)