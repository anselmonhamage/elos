# Elos

Plataforma web de homenagens e mural de recados de aniversario.

---

## Funcionalidades

- Galeria de Boas-Vindas com carrossel horizontal de fotos
- Mensagem especial editavel
- Terminal interativo Dev com comandos personalizados
- Mural de recados com curtidas em tempo real
- Sistema de permissoes: Administrador, Escritor, Leitor

---

## Tecnologias

- Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Flask-WTF
- SQLite
- HTML5, CSS3 Vanilla, JavaScript ES6+ (modulos)

---

## Como executar localmente

### 1. Clonar o repositorio

```bash
git clone https://github.com/anselmonhamage/elos.git
cd elos
```

### 2. Criar e ativar o ambiente virtual

Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variaveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
SECRET_KEY=sua_chave_secreta_super_segura
ADMIN_NAME="Administrador Principal"
ADMIN_EMAIL="admin@dev.com"
ADMIN_PASSWORD="AdminPass123!"
```

### 5. Correr as migracoes

Na primeira execucao, aplique as migracoes para criar o schema do banco de dados:

```bash
flask db upgrade
```

Para criar um novo arquivo de migracao apos alterar os modelos:

```bash
flask db migrate -m "descricao da alteracao"
flask db upgrade
```

### 6. Inicializar dados base (roles e admin)

```bash
flask init-db
```

### 7. Iniciar em modo desenvolvimento

```bash
python app.py
```

Acesse: `http://127.0.0.1:5000`

---

## Producao com Gunicorn

O projeto inclui o arquivo `wsgi.py` como entrypoint para servidores WSGI.

### Instalacao

O Gunicorn ja esta incluido no `requirements.txt`. Para instalar manualmente:

```bash
pip install gunicorn
```

### Executar com Gunicorn

```bash
gunicorn wsgi:app
```

### Configuracao recomendada para producao

```bash
gunicorn wsgi:app \
  --workers 4 \
  --bind 0.0.0.0:5000 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

Parametros:

| Parametro | Descricao |
|---|---|
| `--workers` | Numero de processos worker. Recomendado: `(2 x num_cpus) + 1` |
| `--bind` | Endereco e porta de escuta |
| `--timeout` | Tempo maximo em segundos por request |
| `--access-logfile` | Ficheiro de log de acessos |
| `--error-logfile` | Ficheiro de log de erros |

### Executar com um ficheiro de configuracao

Crie um ficheiro `gunicorn.conf.py` na raiz do projeto:

```python
bind = "0.0.0.0:5000"
workers = 4
timeout = 120
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
```

E inicie com:

```bash
gunicorn -c gunicorn.conf.py wsgi:app
```

---

## Estrutura do projeto

```
elos/
├── controllers/          # Logica de controle e rotas
├── forms/                # Validacao de formularios WTForms
├── models/               # Modelos SQLAlchemy
├── static/               # Ficheiros estaticos
│   ├── css/
│   ├── images/
│   ├── js/
│   └── uploads/          # Fotos enviadas pelos utilizadores (ignorado no Git)
├── templates/            # Templates HTML Jinja2
│   ├── components/
│   └── modals/
├── app.py                # Ponto de entrada Flask
├── wsgi.py               # Entrypoint para producao (Gunicorn)
├── requirements.txt      # Dependencias do projeto
├── .env.example          # Exemplo de variaveis de ambiente
├── LICENSE               # Licenca MIT
└── README.md
```

---

## Licenca

Licenciado sob a licenca MIT. Consulte o ficheiro [LICENSE](LICENSE) para mais detalhes.
