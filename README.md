# TRÓPICO

E-commerce e sistema administrativo para uma marca brasileira de streetwear. O MVP conecta HTML/CSS/JavaScript puro ao Flask e a um banco relacional, com catálogo, variantes, estoque, carrinho persistente, checkout, pagamento simulado, pedidos e gestão.

## Tecnologias

- Python 3.11+, Flask e Blueprints
- SQLAlchemy, Flask-Migrate e MySQL/PyMySQL
- Flask-Login, hash de senha Werkzeug e proteção CSRF
- HTML5, CSS3 responsivo e JavaScript puro

## Estrutura

```text
app/
├── models/       # entidades e relacionamentos
├── routes/       # auth, loja, carrinho, pedidos e admin
├── services/     # pagamento e frete simulados/substituíveis
├── templates/    # apresentação Jinja
├── static/       # CSS e JavaScript
└── utils/        # autorização
config.py
run.py
```

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` e defina uma `SECRET_KEY` forte.

### MySQL

Crie o banco e usuário:

```sql
CREATE DATABASE tropico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tropico'@'localhost' IDENTIFIED BY 'uma-senha-forte';
GRANT ALL PRIVILEGES ON tropico.* TO 'tropico'@'localhost';
```

Configure no `.env`:

```env
DATABASE_URL=mysql+pymysql://tropico:uma-senha-forte@localhost/tropico
```

Para demonstração sem MySQL, use `DATABASE_URL=sqlite:///tropico.db`.

## Banco, migrations e dados iniciais

Para iniciar rapidamente com as tabelas e 10 produtos:

```powershell
flask --app run.py seed --reset
```

Para controlar alterações de schema em produção:

```powershell
flask --app run.py db init
flask --app run.py db migrate -m "schema inicial"
flask --app run.py db upgrade
```

## Execução

```powershell
flask --app run.py run --debug
```

Acesse `http://127.0.0.1:5000`.

## Credenciais de demonstração

- Administrador: `admin@tropico.com.br` / `Admin@123`
- Cliente: `cliente@tropico.com.br` / `Cliente@123`
- Cupom: `BEMVINDO10`

Troque as senhas antes de qualquer implantação real.

## Funcionalidades disponíveis

- Cadastro, login, logout, perfil, endereço e recuperação neutra de senha
- Catálogo com busca, categorias e ordenação
- Produtos com variantes relacionais de tamanho, cor e estoque
- Carrinho associado ao usuário e validação de disponibilidade no servidor
- Frete e pagamento simulados em serviços separados, sem dados sensíveis
- Pedido com baixa de estoque, cupom, pagamento e entrega
- Histórico e acompanhamento do pedido pelo cliente
- `/admin` protegido por papel de usuário
- Dashboard, produtos, estoque, pedidos, clientes, cupons e relatórios
- Layout responsivo para desktop, tablet e celular

Integrações reais de OAuth, gateway e transportadora devem substituir os adaptadores simulados quando existirem credenciais válidas.

