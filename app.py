from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req.get('queryResult')['intent']['displayName']
    uuid = req.get('originalDetectIntentRequest')['payload']['tiledesk']['payload']['request']['requester'][
        'uuid_user']
    if req.get('queryResult')['queryText'] == 'Recomeçar' or req.get('queryResult')['queryText'] == 'Voltar ao inicio':
        return {
            "followupEventInput": {
                "name": "inicio",
                "languageCode": "en-US"
            }
        }
        
    match intent_name:
        case 'receita_duvida':
            return {
                "followupEventInput": {
                    "name": "receita_duvida_teste",
                    "languageCode": "en-US"
                }
            }

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
            global celebrities
            if req.get('queryResult')['queryText'] == "Sem preferência":
                celebrities = ""
            else:
                celebrities = req.get('queryResult')['queryText']

        case 'ingredientes':
            global ingredients
            if req.get('queryResult')['queryText'] == "Não precisa":
                ingredients = ""
            else:
                ingredients = req.get('queryResult')['queryText']

            return {
                "fulfillmentText": f"""{'Então você é ' + fd_restrict.lower() if fd_restrict else 'Então você não tem restrições alimentares'}, {' tem até ' + time.lower() + ' para preparar receitas' if time else ' não tem preferência de tempo para receitas'}, {' quer preparar algo ' + taste.lower() if taste else ' não tem preferência por gosto específico'}, {'quer auxílio de ' + celebrities if celebrities else ' não tem preferência por canal ou celebridade Globo'}, {' e têm ' + ingredients.lower() + ' na cozinha?' if ingredients else ' e não tem ingredientes adicionais?'}""",
                "source": 'webhook'
            }

        case 'reiniciar':
            return {
                "fulfillmentText": "Recomeçando...",
                "followupEventInput": {
                    "name": "inicio",
                    "languageCode": "en-US"
                }
            }


if __name__ == '__main__':
    app.run(debug=True)
