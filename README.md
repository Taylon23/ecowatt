
## 📊 EcoWatt
EcoWatt é um sistema de economia de energia desenvolvido com Django. Ele permite que os usuários monitorem o consumo de energia de seus equipamentos, acompanhem relatórios mensais e recebam sugestões de melhorias para otimizar o uso de energia.
## 🚀 Funcionalidades

- Monitoramento de consumo
- Relatórios personalizados
- Sugestões de economia
- Interface amigável

## 🛠️ Tecnologias Utilizadas
- Framework: Django
- Frontend: HTML, CSS, Bootstrap
- Banco de Dados: SQLite (pode ser configurado - para PostgreSQL ou MySQL)

## 📊 EcoWatt
EcoWatt é um sistema de economia de energia desenvolvido com Django. Ele permite que os usuários monitorem o consumo de energia de seus equipamentos, acompanhem relatórios mensais e recebam sugestões de melhorias para otimizar o uso de energia.
## Instalação

Clone o repositorio

```bash
git clone https://github.com/Taylon23/ecowatt.git
cd ecowatt

```
Crie e ative um ambiente virtual:

```bash
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate     # Windows  

```
Instale as dependências:

```bash
pip install -r requirements.txt
```
Aplique as migrações:
```bash
python manage.py migrate
```
Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver

```
Acesse o sistema no navegador: http://localhost:8000