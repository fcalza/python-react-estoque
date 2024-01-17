# Entrar no server-python
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug


# FRONT
sudo apt-get update
sudo apt-get install nodejs
sudo apt-get install npm
npm install axios ##https://www.npmjs.com/package/axios
npm i react-router-dom ##https://www.npmjs.com/package/react-router-dom
npm install react-datepicker
npm install moment
npm install
npm start


#sugestões de banco
# tabela para tipo
# tabela auxiliar para quantidades se for escalar mto


# mysql -u root -p
# show databases
# use estoque
# select + from mercadoria


#validação campos vazios e padrões diferentes
#remover adiciona um boolean ao invés de fazer o delete
#ordenação campos
#separar duas tabelas para log? volume?
#validador de datas
#usar bibliotecas HTTP para response python
#setar timezone nas configs
#utilizar models pydantic com validators e 