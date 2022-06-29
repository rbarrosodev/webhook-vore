from flask import Flask, request
import sys
import logging
import json

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://ijmxmeayhtflcc:33d7017fb56b23507daf2fdb24812ec33582e17b54977b787b467768f2d67c33@ec2-23-23-182-238.compute-1.amazonaws.com:5432/dcc9e4h4tek2jj'


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req.get('queryResult')['intent']['displayName']
    if req.get('queryResult')['queryText'] == 'bla':
        return {
            "followupEventInput": {
                "name": "bla",
                "languageCode": "en-US"
            }
        }
    match intent_name:
        case 'fallback':
            if '@' in req.get('queryResult')['queryText']:
                return {
                    "fulfillmentText": 'Obrigado pela sua participação!',
                    "source": 'webhook'
                }
            else:
                return {
                    "fulfillmentText": 'Não entendi... Você pode repetir por favor?',
                    "source": 'webhook'
                }
        case 'restrição_alimentar':
            global fd_restrict
            if req.get('queryResult')['queryText'] == "Não tenho":
                fd_restrict = ""
            else:
                fd_restrict = req.get('queryResult')['queryText']
        case 'tempo':
            global time
            if req.get('queryResult')['queryText'] == "Não precisa":
                time = ""
            else:
                time = req.get('queryResult')['queryText']
        case 'gosto':
            global taste
            if req.get('queryResult')['queryText'] == "Sem preferência":
                taste = ""
            else:
                taste = req.get('queryResult')['queryText']
        case 'celebridades':
            global portions
            if req.get('queryResult')['queryText'] == "Não precisa":
                portions = ""
            else:
                portions = req.get('queryResult')['queryText']
        case 'nomedascelebridades':
            global celebrity_name
            if req.get('queryResult')['queryText'] == "Sem preferência":
                celebrity_name = ""
            else:
                celebrity_name = req.get('queryResult')['queryText']
        case 'ingredientes':
            global ingredients
            if req.get('queryResult')['queryText'] == "Não precisa":
                ingredients = ""
            else:
                ingredients = req.get('queryResult')['queryText']

            return {
                "fulfillmentText": 'funcionou',
                "source": 'webhook'
            }
        case 'restart':
            return {
                "fulfillmentText": "Recomeçando...",
                "followupEventInput": {
                    "name": "inicio",
                    "languageCode": "en-US"
                }
            }


app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(debug=True)
