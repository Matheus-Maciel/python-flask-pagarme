from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, validators, ValidationError, Label
 
class TransactionForm(FlaskForm):
  #Dados do cliente
  name = TextField("Nome",  [validators.Required("Insira seu nome")])
  country = TextField("País",  [validators.Required("Insira o país")])
  email = TextField("Email",  [validators.Required("Por favor preencha seu email.")])
  cpf = IntegerField("Cpf",  [validators.Required("Apenas números no campo CPF.")])
  
  #Dados da compra
  amount = IntegerField("Valor",  [validators.Required("Apenas números no campo valor.")])
  card_holder_name = TextField("Nome (Como está no cartão)",  [validators.Required("Insira seu nome")])
  card_number = IntegerField("Número do cartão",  [validators.Required("Apenas números no campo número do cartão.")])
  card_cvv = IntegerField("Código de Segurança",  [validators.Required("Apenas números no campo código de segurança.")])
  card_expiration_date = IntegerField("Data de Expiração",  [validators.Required("Apenas números no campo data de expiração.")])

  #Informações para envio
  scountry = TextField("País",  [validators.Required("Insira o país")])
  state = TextField("Estados",  [validators.Required("Insira o estado")])
  city = TextField("Cidade",  [validators.Required("Insira a cidade")])
  neighborhood = TextField("Bairro",  [validators.Required("Insira o bairro")])
  street = TextField("Rua",  [validators.Required("Insira a rua")])
  street_number = IntegerField("Número",  [validators.Required("Apenas número do campo número")])
  zipcode = IntegerField("CEP",  [validators.Required("Apenas números no campo CEP.")])
  
  message = TextAreaField("Message")
  submit = SubmitField("Enviar")

class BalanceForm(FlaskForm):
  disponivel = Label("disponivel","text")
  transferido = Label("transferido","text")
  receber = Label("receber","text")


