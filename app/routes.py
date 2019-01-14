from flask import Flask #Importando a classe FLASK
from flask import jsonify #Módulo Flask para JSON
from flask import render_template #Módulo Flask para HTML
from flask import request #Módulo que determina o método HTTP (GET ou POST)
from flask import flash #Módulo para exibit popups

from forms import TransactionForm #Importa a classe criada em FORMS.PY
from forms import BalanceForm #Importa a classe criada em FORMS.PY

import pagarme
pagarme.authentication_key('ak_test_1bJgehkFPIQwihtavxJ0Ko7GCRKcYu')

app = Flask(__name__) #Instância o Flask

app.secret_key = 'development key' #Chave de desenvolvimento

@app.route('/', methods=['GET'])#Responsável por interpretar a rota/url
def home():
    #return "Hello", 200
    #return jsonify({"mensage":"Hello JSON!"})
    return render_template("home.html") #Renderizando home.html fazendo uso do módulo render_template

@app.route('/about', methods=['GET'])
def about():
  return render_template('about.html')

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    form = TransactionForm()
    if request.method == 'POST':
        if form.validate()==False:
            flash('Preencha todos os campos')
            return render_template('transaction.html', form=form)
        else:
            #Para capturar o conteúdo dos campos str(form.name.data)
            #Captura dos dados digitados e envio para o endpoint da pagar.me
            params = {
                   "amount": int(int(form.amount.data)*100), #Valor da transação em centavos
               "card_number": str(form.card_number.data), #Número do cartão de crédito
               "card_cvv": str(form.card_cvv.data), #Código de segurança do cartão de crédito
               "card_expiration_date": str(form.card_expiration_date.data), #Data de expiração do cartão (somente números)
               "card_holder_name": str(form.card_holder_name.data), #Nome do titular do cartão
               "customer": { #Informações do cliente
                 "external_id": "#0001",
                 "name": str(form.name.data),
                 "type": "individual",
                 "country": str(form.country.data),
                 "email": str(form.email.data),
                "documents": [ #Documento do cliente (necessário para o antifraude)
                   {
                     "type": "cpf",
                     "number": str(form.cpf.data)
                   }
                 ],
                 "phone_numbers": ["+5511999998888"],
                 "birthday": "1984-12-03"
               },
               "billing": { #Informações da cobrança (Obrigatório com antifraude)
                 "name": "Capsule Corp", #Entidade de cobrança
                 "address": { #Endereço de cobrança
                 "country": "jp",
                 "state": "Chiyoda",
                 "city": "Tokyo",
                 "neighborhood": "Shogakukan",
                 "street": "Jinbo Cho",
                 "street_number": "3-13",
                 "zipcode": "1000001"
                 }
               },
               "shipping": { #Informações de envio para bens físicos
                 "name": "Capsule Corp", #Entidade de cobrança
                 "fee": "1000", #Custo do envio
                 "delivery_date": "2019-01-14", #Data de entrega no formato YYYY-MM-DD
                 "expedited": True, #Entrega expressa (true or false)
                 "address": { #Endereço de envio
                 "country": str(form.scountry.data),
                 "state": str(form.state.data),
                 "city": str(form.city.data),
                 "neighborhood": str(form.neighborhood.data),
                 "street": str(form.street.data),
                 "street_number": str(form.street_number.data),
                 "zipcode": str(form.zipcode.data)
                 }
               },
               "items": [ #Informações do itens comprados
                 {
                   "id": "c123", #SKU (Unidade de manutenção de estoque) ou número de identificação da loja
                   "title": "Nuvem voadora", #Nome do item vendido
                   "unit_price": int(int(form.amount.data)*100), #Preço unitário
                   "quantity": "1", #Quantidade
                   "tangible": True #Bem tangivel (true or false)
                 }
               ],
            #https://docs.pagar.me/v3/docs/split-rules

               "split_rules": [ #Informações de dois recebedores (split_rule)
               {
                 "recipient_id": "re_cjqmnxj8o002ywv6e3guj9zbj", #Id do recebedor
                 "percentage": 50, #Porcentagem da transação que irá pro recebedor (Sempre valores redondos 40, 50, 60, etc) pode ser substituído por amount
                 "liable": True, #Se assume os riscos de chargeback (ao menos um deve estar como true)
                 "charge_processing_fee": True #Se será cobrado pelas taxas de transação (ao menos um deve estar como true)
               },{
                 "recipient_id": "re_cjq867x4m01fl2p6dq9i32ttf",
                 "percentage": 50,
                 "liable": True, #Está errado na documentação, o true está minúsculo
                 "charge_processing_fee": True #Está errado na documentação, o true está minúsculo
               }
             ]
            }
            try:
                transaction = pagarme.transaction.create(params)
            except:
                return render_template('transaction-fail.html', form=form)
                
            #Fim da interação com a API da Pagar.me

            return render_template('transaction-complete.html', form=form)
    elif request.method == 'GET':
        return render_template('transaction.html', form=form)

@app.route('/balance', methods=['GET'])
def balance():
    form = BalanceForm()

    #Aqui começa a interação com a API da Pagar.me
    balance = pagarme.balance.default_recipient_balance()
    sdisponivel = balance["available"]
    # Aqui se encerra a interação com a API da Pagar.me
    
    sdisponivel = sdisponivel["amount"]

    stransferido = balance["transferred"]
    stransferido = stransferido["amount"]

    sreceber = balance["waiting_funds"]
    sreceber = sreceber["amount"]
    
    form.disponivel = sreceber/100
    form.transferido = stransferido/100
    form.receber = sreceber/100
    
    return render_template('balance.html', form=form)

if __name__ == '__main__':
    app.run(debug=True) #Executa o servidor local
