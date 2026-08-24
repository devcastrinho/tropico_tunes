# TRÓPICO

## Versão estática para GitHub Pages

A raiz deste repositório agora contém uma versão estática e funcional da loja, pronta para o GitHub Pages. Ela preserva o mesmo front-end e oferece catálogo, busca, filtros, página de produto, variações, sacola persistente, cupom `BEMVINDO10`, checkout demonstrativo, conta local, histórico de pedidos e modo claro/escuro.

Como o GitHub Pages não executa banco de dados nem Python, os dados da sacola, da conta e dos pedidos ficam no `localStorage` do navegador. O checkout é apenas uma demonstração e não realiza cobranças ou envios reais.

Para visualizar localmente:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Depois, abra <http://127.0.0.1:8765/>.

Arquivos principais da versão estática:

```text
index.html              # página inicial
produtos/               # catálogo, busca, filtros e ordenação
produto/                # detalhes, tamanhos e cores
carrinho/               # sacola persistente
checkout/               # cupom e pedido demonstrativo
conta/                  # perfil local e histórico de pedidos
assets/js/store.js      # dados e comportamento da loja
assets/css/             # estilos específicos da versão estática
```

---

E-commerce e sistema administrativo para uma marca brasileira de streetwear. O MVP conecta HTML/CSS/JavaScript puro ao Flask e a um banco relacional, com catálogo, variantes, estoque, carrinho persistente, checkout, pagamento simulado, pedidos e gestão.

> O terminal serve apenas para iniciar o servidor. Depois disso, a loja e o painel são utilizados pelo navegador em `http://127.0.0.1:5000`.

## Como usar

O guia completo para instalação, acesso à loja, checkout e painel administrativo está em **[COMO_USAR.md](COMO_USAR.md)**.

No Windows, após concluir a primeira instalação, também é possível iniciar o sistema dando dois cliques em **`iniciar.bat`**. A janela aberta deve permanecer em execução enquanto o site estiver sendo utilizado.

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

### Opção 1 — atalho no Windows

Dê dois cliques em `iniciar.bat` e abra <http://127.0.0.1:5000>.

### Opção 2 — terminal

```powershell
flask --app run.py run --debug
```

Acesse <http://127.0.0.1:5000>. O terminal precisa permanecer aberto porque ele mantém o servidor em funcionamento. Para encerrar, pressione `Ctrl + C`.

> O GitHub Pages publica a versão estática da raiz do repositório. O sistema Flask abaixo continua disponível para desenvolvimento local quando forem necessários banco de dados e painel administrativo.

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
