from flask import Flask, request
import pandas as pd

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req.get('queryResult')['intent']['displayName']
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
            df = pd.read_csv("data.csv",
                             delimiter=';',
                             skipinitialspace=True)
            uuid = req.get('originalDetectIntentRequest')['payload']['tiledesk']['payload']['request']['requester']['uuid_user']
            df2 = {'uuid': uuid}
            if df[df['uuid'] == uuid].empty:
                df = df.append(df2, ignore_index=True)
                print(df)
                df.to_csv('data.csv', index=False, sep=";")

            if req.get('queryResult')['queryText'] != "Não tenho":
                df = pd.read_csv("data.csv",
                                 delimiter=';',
                                 skipinitialspace=True)
                df.at[df[df['uuid'] == uuid].index.values[0], 'fdr'] = req.get('queryResult')['queryText']
                print(df)
                df.to_csv('data.csv', index=False, sep=";")


        case 'tempo':
            if req.get('queryResult')['queryText'] != "Não precisa":
                uuid = req.get('originalDetectIntentRequest')['payload']['tiledesk']['payload']['request']['requester']['uuid_user']
                df = pd.read_csv("data.csv",
                                 delimiter=';',
                                 skipinitialspace=True)
                df.at[df[df['uuid'] == uuid].index.values[0], 'time'] = req.get('queryResult')['queryText']
                print(df)
                df.to_csv('data.csv', index=False, sep=";")

        case 'gosto':
            if req.get('queryResult')['queryText'] != "Sem preferência":
                uuid = req.get('originalDetectIntentRequest')['payload']['tiledesk']['payload']['request']['requester']['uuid_user']
                df = pd.read_csv("data.csv",
                                 delimiter=';',
                                 skipinitialspace=True)
                df.at[df[df['uuid'] == uuid].index.values[0], 'taste'] = req.get('queryResult')['queryText']
                print(df)
                df.to_csv('data.csv', index=False, sep=";")

        case 'celebridades':
            if req.get('queryResult')['queryText'] != "Sem preferência":
                uuid = req.get('originalDetectIntentRequest')['payload']['tiledesk']['payload']['request']['requester']['uuid_user']
                df = pd.read_csv("data.csv",
                                 delimiter=';',
                                 skipinitialspace=True)
                df.at[df[df['uuid'] == uuid].index.values[0], 'celeb'] = req.get('queryResult')['queryText']
                print(df)
                df.to_csv('data.csv', index=False, sep=";")

        case 'ingredientes':
            if req.get('queryResult')['queryText'] != "Não precisa":
                uuid = req.get('originalDetectIntentRequest')['payload']['tiledesk']['payload']['request']['requester']['uuid_user']
                df = pd.read_csv("data.csv",
                                 delimiter=';',
                                 skipinitialspace=True)
                df.at[df[df['uuid'] == uuid].index.values[0], 'ing'] = req.get('queryResult')['queryText']
                print(df)
                df.to_csv('data.csv', index=False, sep=";")

                uindex = df[df['uuid'] == uuid].index.values[0]

                return {
                    "fulfillmentText": f"""{'Então você é ' + str(df.at[uindex, 'fdr']).lower() if str(df.at[uindex, 'fdr']) != 'nan' else 'Então você não tem restrições alimentares'}, {' tem até ' + str(df.at[uindex, 'time']).lower() + ' para preparar receitas' if str(df.at[uindex, 'time']) != 'nan' else ' não tem preferência de tempo para receitas'}, {' quer preparar algo ' + str(df.at[uindex, 'taste']).lower() if str(df.at[uindex, 'taste']) != 'nan' else ' não tem preferência por gosto específico'}, {'quer auxílio de ' + str(df.at[uindex, 'celeb']) if str(df.at[uindex, 'celeb']) != 'nan' else ' não tem preferência por canal ou celebridade Globo'}, {' e têm ' + str(df.at[uindex, 'ing']).lower() + ' na cozinha?' if str(df.at[uindex, 'ing']) != 'nan' else ' e não tem ingredientes adicionais?'}""",
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
