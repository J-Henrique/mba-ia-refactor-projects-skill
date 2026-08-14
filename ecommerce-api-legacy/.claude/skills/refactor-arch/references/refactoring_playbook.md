# Playbook de Refatoração

Este playbook contém padrões concretos de transformação para corrigir cada anti-pattern do catálogo e mover o projeto para o padrão MVC.

Cada padrão apresenta exemplos de código **antes** (legado) e **depois** (refatorado), com exemplos para Python/Flask e Node.js/Express quando aplicável.

---

## 1. Extração de Hardcoded Credentials

**Severidade:** CRITICAL
**Anti-pattern:** Hardcoded Credentials

> ⚠️ **Regra fundamental:** O fallback de `os.environ.get()` ou `process.env` NUNCA pode conter credenciais reais. Use string vazia ou um placeholder óbvio (`'CHANGE_ME'`). Se a variável de ambiente não estiver configurada, a aplicação deve falhar ao iniciar — não usar um valor real "só para funcionar".

### Antes — ❌ Errado (credenciais reais no código)

**Python/Flask — `app.py`:**
```python
app.config['SECRET_KEY'] = 'minha-chave-super-secreta-123'
app.config['DATABASE_URI'] = 'sqlite:///data.db'
```

**Node.js/Express — `AppManager.js`:**
```javascript
const GATEWAY_KEY = 'sk_live_1234567890abcdef';
const DB_PASSWORD = 'admin123';
```

### Depois — ✅ Correto (valores placeholder ou sem fallback)

**Python/Flask — `config/settings.py`:**
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # sem fallback — falha se não configurado
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///data.db')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
```

**Node.js/Express — `config/config.js`:**
```javascript
require('dotenv').config();

module.exports = {
    gatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    dbPassword: process.env.DB_PASSWORD,
    port: parseInt(process.env.PORT, 10) || 3000,
};
```

### ❌ Padrão incorreto — não fazer

```javascript
// ERRO: fallback com credencial REAL — mesma vulnerabilidade que ter hardcoded
gatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'pk_live_1234567890abcdef',
dbPass: process.env.DB_PASS || 'senha_super_secreta_prod_123',
```

---

## 2. Remoção de Log de Dados Sensíveis

**Severidade:** HIGH
**Anti-pattern:** Sensitive Data Logging

> ⚠️ **Regra fundamental:** NUNCA logar números de cartão de crédito completos, senhas, chaves de API ou tokens de autenticação. Quando necessário para auditoria, mascare os dados (ex: exibir apenas os 4 últimos dígitos).

### Antes — ❌ Errado (dados sensíveis no log)

**Node.js/Express — `CheckoutController.js`:**
```javascript
console.log(`Processando cartão ${card} na chave ${paymentGatewayKey}`);
console.log(`Salvando no cache: ${key}`);
```

**Python/Flask — `controllers.py`:**
```python
print(f"Processando pagamento: cartao {card_number}, chave {gateway_key}")
```

### Depois — ✅ Correto (logs sanitizados ou removidos)

**Node.js/Express — `CheckoutController.js`:**
```javascript
// ✅ Remove log de dados sensíveis completamente
// Se precisar de auditoria, use apenas os 4 últimos dígitos:
console.log(`Processando pagamento para cartão terminado em ${card.slice(-4)}`);

// ✅ Log estruturado sem dados sensíveis (se necessário para debug)
logger.info('Checkout iniciado', {
    userId: user.id,
    courseId,
    enrollmentId,
});
```

**Python/Flask — `controllers/produto_controller.py`:**
```python
import logging
logger = logging.getLogger(__name__)

# ✅ Use logger estruturado em vez de print
logger.info('Checkout processado', extra={
    'usuario_id': user_id,
    'curso_id': curso_id,
})
```

---

## 3. Extração de Lógica de Controller (Fat Controller → MVC)

**Severidade:** HIGH
**Anti-pattern:** Fat Controller

### Antes

**Python/Flask — `app.py` (lógica de negócio na rota):**
```python
@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()
    if not data or not data.get('nome'):
        return jsonify({'erro': 'Dados invalidos'}), 400
    # Lógica SQL direto na rota
    cursor = get_db().cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)",
                   (data['nome'], data['preco']))
    get_db().commit()
    return jsonify({'id': cursor.lastrowid}), 201
```

**Node.js/Express — `AppManager.js` (lógica de negócio na rota):**
```javascript
app.post('/api/checkout', (req, res) => {
    let u = req.body.usr;
    let e = req.body.eml;
    let p = req.body.pwd;
    // Lógica de pagamento, criação de usuário, matrícula TUDO aqui
    if (!u || !e || !cid) return res.status(400).send("Bad Request");
    this.db.get("SELECT * FROM courses WHERE id = ?", [cid], (err, course) => {
        // ... callbacks aninhados, validação, persistência ...
    });
});
```

### Depois

**Python/Flask — `controllers/produto_controller.py`:**
```python
from models.produto_model import ProdutoModel

class ProdutoController:
    @staticmethod
    def criar_produto(data):
        if not data or not data.get('nome'):
            return {'erro': 'Dados invalidos'}, 400
        produto_id = ProdutoModel.criar(data['nome'], data.get('preco', 0))
        return {'id': produto_id}, 201
```

**Python/Flask — `routes/routes.py`:**
```python
from controllers.produto_controller import ProdutoController

@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    return ProdutoController.criar_produto(request.get_json())
```

**Node.js/Express — `controllers/CheckoutController.js`:**
```javascript
const UserModel = require('../models/UserModel');
const PaymentService = require('../services/PaymentService');

class CheckoutController {
    async checkout(req, res) {
        try {
            const { usr, eml, pwd, c_id, card } = req.body;
            if (!usr || !eml || !c_id || !card) {
                return res.status(400).json({ error: 'Bad Request' });
            }
            const result = await PaymentService.processCheckout(usr, eml, pwd, c_id, card);
            return res.status(200).json(result);
        } catch (err) {
            return res.status(500).json({ error: err.message });
        }
    }
}
```

---

## 4. Extração de Model (God Class → Models)

**Severidade:** CRITICAL
**Anti-pattern:** God Class

### Antes

**Python/Flask — `models.py` (tudo junto, 350 linhas, 4 domínios):**
```python
def get_produtos():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM produtos")
    return cursor.fetchall()

def get_usuarios():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios")
    return cursor.fetchall()

def get_pedidos_usuario(usuario_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ?", (usuario_id,))
    pedidos = cursor.fetchall()
    for pedido in pedidos:
        cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = ?", (pedido['id'],))
        pedido['itens'] = cursor.fetchall()  # N+1 queries
    return pedidos
```

### Depois

**Python/Flask — `models/produto_model.py`:**
```python
from database import get_db

class ProdutoModel:
    @staticmethod
    def listar_todos():
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM produtos")
        return cursor.fetchall()

    @staticmethod
    def buscar_por_id(produto_id):
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        return cursor.fetchone()

    @staticmethod
    def criar(nome, preco):
        cursor = get_db().cursor()
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
        get_db().commit()
        return cursor.lastrowid
```

**Python/Flask — `models/pedido_model.py`:**
```python
from database import get_db

class PedidoModel:
    @staticmethod
    def listar_por_usuario(usuario_id):
        db = get_db()
        cursor = db.cursor()
        # JOIN resolve N+1
        cursor.execute("""
            SELECT p.id, p.usuario_id, p.data, p.status,
                   GROUP_CONCAT(ip.produto_id || ':' || ip.quantidade) as itens
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
            WHERE p.usuario_id = ?
            GROUP BY p.id
        """, (usuario_id,))
        return cursor.fetchall()
```

**Node.js/Express — `models/Database.js`:**
```javascript
const sqlite3 = require('sqlite3').verbose();
const { promisify } = require('util');

class Database {
    constructor(dbPath = ':memory:') {
        this.db = new sqlite3.Database(dbPath);
        this.run = promisify(this.db.run.bind(this.db));
        this.get = promisify(this.db.get.bind(this.db));
        this.all = promisify(this.db.all.bind(this.db));
    }
}

module.exports = Database;
```

---

## 5. Implementação de Middleware / Error Handler Centralizado

**Severidade:** MEDIUM
**Anti-pattern:** Tratamento de erros inconsistente

### Antes

**Python/Flask — `controllers.py`:**
```python
@app.route('/api/produtos/<int:id>')
def get_produto(id):
    try:
        produto = get_produto_por_id(id)
        if not produto:
            return jsonify({'erro': 'Produto nao encontrado'}), 404
        return jsonify(produto)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500  # Vaza detalhes internos
```

**Node.js/Express — `AppManager.js`:**
```javascript
app.get('/api/users/:id', (req, res) => {
    try {
        // ...
    } catch (err) {
        res.status(500).send("Erro interno");  // Texto puro, sem JSON
    }
});
```

### Depois

**Python/Flask — `middlewares/error_handler.py`:**
```python
from flask import jsonify

class AppError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({'erro': error.message}), error.status_code

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        app.logger.error(f'Erro interno: {error}', exc_info=True)
        return jsonify({'erro': 'Erro interno do servidor'}), 500
```

**Node.js/Express — `middlewares/errorHandler.js`:**
```javascript
function errorHandler(err, req, res, next) {
    console.error(`[ERROR] ${err.message}`, err.stack);
    const status = err.statusCode || 500;
    res.status(status).json({
        error: err.message || 'Internal Server Error',
    });
}

module.exports = errorHandler;
```

---

## 6. Substituição de API Deprecated / Criptografia Insegura

**Severidade:** HIGH
**Anti-pattern:** Deprecated API

### Antes

**Python — `utils/helpers.py`:**
```python
import hashlib

def hash_password(password):
    # MD5 é inseguro e deprecated
    return hashlib.md5(password.encode()).hexdigest()
```

**Node.js — `utils.js`:**
```javascript
// Criptografia caseira insegura
function badCrypto(password) {
    let hash = '';
    for (let i = 0; i < password.length; i++) {
        hash += String.fromCharCode(password.charCodeAt(i) ^ 0x2A);
    }
    return btoa(hash);
}
```

### Depois

**Python — `utils/security.py`:**
```python
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

**Node.js — `utils/security.js`:**
```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 10;

async function hashPassword(password) {
    return await bcrypt.hash(password, SALT_ROUNDS);
}

async function comparePassword(password, hash) {
    return await bcrypt.compare(password, hash);
}

module.exports = { hashPassword, comparePassword };
```

---

## 7. Injeção de Dependência

**Severidade:** HIGH
**Anti-pattern:** Tight Coupling

### Antes

**Python/Flask — `controllers.py`:**
```python
from database import get_db

def listar_produtos():
    db = get_db()  # Acoplamento direto — impossível mockar em testes
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos")
    return cursor.fetchall()
```

**Node.js/Express — `AppManager.js`:**
```javascript
class AppManager {
    constructor() {
        this.db = new sqlite3.Database(':memory:');  // DB criado dentro da classe
    }
}
```

### Depois

**Python/Flask — `controllers/produto_controller.py`:**
```python
class ProdutoController:
    def __init__(self, produto_model):
        self.produto_model = produto_model  # Injeção via construtor

    def listar(self):
        return self.produto_model.listar_todos()
```

**Python/Flask — `app.py` (composition root):**
```python
from models.produto_model import ProdutoModel
from controllers.produto_controller import ProdutoController

produto_model = ProdutoModel()
produto_controller = ProdutoController(produto_model)
```

**Node.js/Express — `app.js` (composition root):**
```javascript
const Database = require('./models/Database');
const UserController = require('./controllers/UserController');
const CheckoutController = require('./controllers/CheckoutController');

const db = new Database(process.env.DB_PATH || ':memory:');
const userController = new UserController(db);
const checkoutController = new CheckoutController(db);
```

---

## 8. Centralização de Configurações

**Severidade:** MEDIUM
**Anti-pattern:** Configurações dispersas

### Antes

**Python/Flask — `app.py`:**
```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha-chave-super-secreta-123'
app.config['DEBUG'] = True
app.config['DATABASE'] = 'sqlite:///data.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_COOKIE_HTTPONLY'] = True
```

**Node.js/Express — `app.js`:**
```javascript
const PORT = 3000;
const GATEWAY_KEY = 'sk_live_abc123';
const DB_PATH = ':memory:';
```

### Depois

**Python/Flask — `config/settings.py`:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    DATABASE = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

**Node.js/Express — `config/config.js`:**
```javascript
require('dotenv').config();

module.exports = {
    port: parseInt(process.env.PORT, 10) || 3000,
    gatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    dbPath: process.env.DB_PATH || ':memory:',
    jwtSecret: process.env.JWT_SECRET,
    corsOrigins: (process.env.CORS_ORIGINS || '').split(','),
};
```

---

## 9. Remoção de Duplicate Code

**Severidade:** MEDIUM
**Anti-pattern:** Duplicate Code

### Antes

**Python/Flask — `controllers.py` (validação repetida em cada endpoint):**
```python
@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Dados invalidos'}), 400
    if not data.get('nome'):
        return jsonify({'erro': 'Nome é obrigatorio'}), 400
    # ...

@app.route('/api/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Dados invalidos'}), 400
    if not data.get('nome'):
        return jsonify({'erro': 'Nome é obrigatorio'}), 400
    # ...
```

**Node.js/Express — `AppManager.js` (verificação de autenticação repetida):**
```javascript
app.get('/api/users', (req, res) => {
    if (!req.headers.authorization) return res.status(401).send("Unauthorized");
    // ...
});

app.post('/api/checkout', (req, res) => {
    if (!req.headers.authorization) return res.status(401).send("Unauthorized");
    // ...
});
```

### Depois

**Python/Flask — `utils/validators.py`:**
```python
from functools import wraps
from flask import request, jsonify

def validar_json(*campos_obrigatorios):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'erro': 'Dados invalidos'}), 400
            for campo in campos_obrigatorios:
                if not data.get(campo):
                    return jsonify({'erro': f'{campo} é obrigatorio'}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/produtos', methods=['POST'])
@validar_json('nome', 'preco')
def criar_produto():
    # Lógica limpa — validação já foi feita pelo decorator
    pass
```

**Node.js/Express — `middlewares/auth.js`:**
```javascript
function requireAuth(req, res, next) {
    if (!req.headers.authorization) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    next();
}

// Aplicado globalmente ou por rota
app.get('/api/users', requireAuth, userController.list);
app.post('/api/checkout', requireAuth, checkoutController.checkout);
```

---

## 10. Correção de SQL Injection

**Severidade:** CRITICAL
**Anti-pattern:** SQL Injection

### Antes

**Python/Flask — `models.py`:**
```python
def buscar_produto(nome):
    cursor = get_db().cursor()
    # Concatenação direta — SQL Injection
    cursor.execute(f"SELECT * FROM produtos WHERE nome LIKE '%{nome}%'")
    return cursor.fetchall()
```

**Node.js/Express — `AppManager.js`:**
```javascript
// Concatenação direta — SQL Injection
db.get(`SELECT * FROM users WHERE email = '${email}'`, (err, user) => { ... });
```

### Depois

**Python/Flask — `models/produto_model.py`:**
```python
def buscar(nome):
    cursor = get_db().cursor()
    # Placeholder parametrizado — SQL Injection não é mais possível
    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f'%{nome}%',))
    return cursor.fetchall()
```

**Node.js/Express — `models/Database.js`:**
```javascript
class Database {
    async getUserByEmail(email) {
        // Placeholder parametrizado
        return await this.get('SELECT * FROM users WHERE email = ?', [email]);
    }
}
```

---

## 11. Correção de N+1 Queries

**Severidade:** MEDIUM
**Anti-pattern:** N+1 Queries

### Antes

**Python/Flask — `models.py`:**
```python
def get_pedidos_usuario(usuario_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ?", (usuario_id,))
    pedidos = cursor.fetchall()
    for pedido in pedidos:  # N queries adicionais dentro do loop
        cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = ?", (pedido['id'],))
        pedido['itens'] = cursor.fetchall()
    return pedidos
```

### Depois

**Python/Flask — `models/pedido_model.py`:**
```python
def get_pedidos_usuario(usuario_id):
    db = get_db()
    cursor = db.cursor()
    # JOIN resolve em uma única query
    cursor.execute("""
        SELECT p.*, ip.id as item_id, ip.produto_id, ip.quantidade, ip.preco
        FROM pedidos p
        LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
        WHERE p.usuario_id = ?
    """, (usuario_id,))
    rows = cursor.fetchall()
    # Agrupa itens por pedido em memória (1 query total)
    pedidos = {}
    for row in rows:
        pedido_id = row['id']
        if pedido_id not in pedidos:
            pedidos[pedido_id] = dict(row)
            pedidos[pedido_id]['itens'] = []
        if row['item_id']:
            pedidos[pedido_id]['itens'].append({
                'id': row['item_id'],
                'produto_id': row['produto_id'],
                'quantidade': row['quantidade'],
                'preco': row['preco'],
            })
    return list(pedidos.values())
```