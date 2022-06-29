from flask import Flask, request
import sys
import logging
import psycopg2
import json


def db_connect():
    con = psycopg2.connect(host='ec2-23-23-182-238.compute-1.amazonaws.com',
                           database='dcc9e4h4tek2jj',
                           user='ijmxmeayhtflcc',
                           password='33d7017fb56b23507daf2fdb24812ec33582e17b54977b787b467768f2d67c33',
                           port='5432')
    return con


def db_insert(sql):
    con = db_connect()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        con.rollback()
        cur.close()
        return 1
    cur.close()


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
                print(req.get('queryResult'))
        case 'tempo':
            global time
            if req.get('queryResult')['queryText'] == "Não precisa":
                time = ""
            else:
                time = req.get('queryResult')['queryText']
                req.get('queryResult')
        case 'gosto':
            global taste
            if req.get('queryResult')['queryText'] == "Sem preferência":
                taste = ""
            else:
                taste = req.get('queryResult')['queryText']
                req.get('queryResult')
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
                "fulfillmentText": f"""{'Então você é ' + fd_restrict.lower() if fd_restrict else 'Então você não tem restrições alimentares'}, {' tem até ' + time.lower() + ' para preparar receitas' if time else ' não tem preferência de tempo para receitas'}, {' quer preparar algo ' + taste.lower() if taste else ' não tem preferência por gosto específico'}, {'quer que renda ' + portions.lower() if portions else ' não tem preferência por tamanho de porção'}, {'quer auxílio de ' + celebrity_name if celebrity_name else ' não tem preferência por canal ou celebridade Globo'}, {' e têm ' + ingredients.lower() + ' na cozinha?' if ingredients else ' e não tem ingredientes adicionais?'}""",
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
