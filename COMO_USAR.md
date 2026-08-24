# Como usar o TRÓPICO

## Loja estática (GitHub Pages)

A versão estática não exige instalação do Flask. Para testá-la no computador, execute na pasta do projeto:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Abra <http://127.0.0.1:8765/>. A sacola, os dados da conta e os pedidos demonstrativos são mantidos somente no navegador. Use o cupom `BEMVINDO10` no checkout. Nenhuma cobrança ou entrega real é criada.

---

O terminal é usado somente para iniciar o servidor Flask. Depois que o servidor estiver ligado, todo o sistema é utilizado normalmente pelo navegador.

## Uso rápido no Windows

Se o projeto já foi instalado, dê dois cliques em `iniciar.bat`.

O terminal permanecerá aberto enquanto o servidor estiver funcionando. Em seguida, abra:

<http://127.0.0.1:5000>

Para desligar o sistema, volte ao terminal e pressione `Ctrl + C`.

## Primeira instalação

Abra o PowerShell dentro da pasta do projeto e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
flask --app run.py seed
```

O comando `seed` cria as tabelas, dez produtos e as contas de demonstração. Ele deve ser executado somente na primeira instalação.

Depois, inicie o servidor:

```powershell
flask --app run.py run --debug
```

## Como entrar

### Loja e conta do cliente

1. Acesse <http://127.0.0.1:5000>.
2. Clique em **Entrar**.
3. Use `cliente@tropico.com.br` e a senha `Cliente@123`.
4. Explore o catálogo, selecione tamanho e cor e adicione produtos à sacola.
5. No checkout, use o cupom `BEMVINDO10` se desejar.
6. Escolha uma forma de pagamento simulada e confirme o pedido.
7. Consulte o andamento em **Meus pedidos**.

### Painel administrativo

1. Entre com `admin@tropico.com.br` e a senha `Admin@123`.
2. Acesse <http://127.0.0.1:5000/admin>.
3. Utilize o menu para gerenciar produtos, estoque, pedidos, clientes, cupons e relatórios.

## Observações importantes

- O pagamento e o frete são simulações de demonstração.
- Nunca informe dados reais de cartão.
- O servidor de desenvolvimento do Flask é adequado apenas para uso local.
- O GitHub Pages publica a loja estática da raiz do repositório. Para usar o painel administrativo, autenticação real, banco de dados ou pagamentos reais, ainda é necessária uma hospedagem compatível com Python/Flask.
