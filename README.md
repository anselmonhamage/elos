# 🎈 Elos - Plataforma de Homenagens & Aniversário Dev

**Elos** é uma aplicação web moderna e interativa desenvolvida em Python/Flask para celebrar comemorações e homenagens a desenvolvedores. O projeto combina um design elegante em estilo dark/glassmorphic com recursos dinâmicos, incluindo carrossel de fotos, terminal interativo e mural de recados com curtidas em tempo real.

---

## ✨ Funcionalidades Principais

- ** Galeria de Boas-Vindas:** Carrossel horizontal em estilo Instagram para exibição de fotos com ajuste visual personalizável (Natural / Preencher). Suporta estado visual com design para quando não houver fotos.
- ** Mensagem Especial:** Espaço dedicado para homenagens poéticas e mensagens inspiradoras.
- ** Terminal Interativo Dev:** Terminal interativo com comandos personalizados e interações sonoras para felicitações no ambiente do desenvolvedor.
- ** Mural de Recados com Curtidas:** Espaço em carrossel horizontal onde convidados e escritores podem publicar recados de aniversário e curtir em tempo real.
- ** Gestão de Conteúdo & Permissões:**
  - **Administrador:** Controle de usuários e gerenciamento completo do sistema.
  - **Escritor:** Permissão para editar seções da tela e publicar novas homenagens.
  - **Leitor:** Acesso à navegação e interações de curtida.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Flask-WTF
- **Banco de Dados:** SQLite
- **Frontend:** HTML5, CSS3 Vanilla (Design System com Glassmorphism & Micro-animações), JavaScript Moderno ES6+ (Módulos)
- **Audio & Efeitos:** Web Audio API & Canvas Confetti

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.
- Git instalado.

### 2. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd elos
```

### 3. Criar e Ativar o Ambiente Virtual
No Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

No Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependências
```bash
pip install -r requirements.txt
```
*(Caso não possua o `requirements.txt`, instale via `pip install flask flask-sqlalchemy flask-migrate flask-login flask-wtf python-dotenv`)*

### 5. Configurar Variáveis de Ambiente
Crie um arquivo `.env` baseado no `.env.example`:
```env
SECRET_KEY=sua_chave_secreta_super_segura
ADMIN_NAME="Administrador Principal"
ADMIN_EMAIL="admin@dev.com"
ADMIN_PASSWORD="AdminPass123!"
```

### 6. Inicializar a Base de Dados
Execute o comando CLI para criar as tabelas e o usuário administrador inicial:
```bash
flask init-db
```

### 7. Iniciar o Servidor de Desenvolvimento
```bash
python app.py
```
Acesse a aplicação no navegador em: `http://127.0.0.1:5000`

---

## 📁 Estrutura do Projeto

```
elos/
├── controllers/          # Lógica de controle e rotas (Main, Auth, Writer, Admin, API)
├── forms/                # Validação de formulários WTForms
├── models/               # Modelos SQLAlchemy (User, TributeContent, Wish)
├── static/               # Arquivos estáticos
│   ├── css/              # Estilos organizados (styles.css)
│   ├── images/           # Logos e imagens padrão do sistema
│   ├── js/               # Módulos JavaScript (Carrosséis, Modais, Interações)
│   └── uploads/          # Diretório de fotos enviadas pelos usuários (Ignorado no Git)
├── templates/            # Gabaritos HTML Jinja2
│   ├── components/       # Passos (Step 1 Boas-vindas, Step 2 Mensagem, etc.)
│   └── modals/           # Modais de login, edição e administração
├── app.py                # Ponto de entrada da aplicação Flask
├── LICENSE               # Licença MIT
├── README.md             # Documentação do projeto
└── .gitignore            # Regras de ignorados no Git
```

---

## 📜 Licença

Este projeto está licenciado sob a Licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
