# Get a Pet — Django

Sistema de adoção de pets desenvolvido em Django + Django REST Framework para a disciplina **Laboratório de Desenvolvimento de Software**.

---

## O que é o projeto

Plataforma web onde tutores publicam pets para adoção e outros usuários podem agendar visitas e concluir o processo de adoção. O sistema possui:

- Autenticação JWT com senha hasheada (PBKDF2)
- API REST completa documentada no Swagger
- Frontend em templates Django (sem React)
- Banco relacional normalizado via Django ORM (SQLite em dev, PostgreSQL em prod)

---

## Arquitetura em Camadas

```
apps/
├── users/
│   ├── models/          ← Entidades ORM (CustomUser)
│   ├── repositories/    ← Queries ORM encapsuladas
│   ├── services/        ← Regras de negócio
│   ├── serializers/     ← Validação e serialização
│   ├── views/           ← Views DRF + views de template
│   └── factories/       ← Factory Pattern (GoF)
└── pets/
    ├── models/          ← Entidades ORM (Pet, PetImage)
    ├── repositories/    ← Queries ORM encapsuladas
    ├── services/        ← Regras de negócio de adoção
    ├── serializers/     ← Validação e serialização
    ├── views/           ← Views DRF + views de template
    └── factories/       ← Factory Pattern (GoF)

patterns/
├── singleton.py         ← Singleton Pattern (GoF): AppConfigService
└── strategies/
    ├── validation_strategy.py  ← Strategy Pattern (GoF): validação
    └── image_strategy.py       ← Strategy Pattern (GoF): upload de imagem
```

---

## Padrões GoF Aplicados

| Padrão | Arquivo | Descrição |
|--------|---------|-----------|
| **Factory** | `apps/users/factories/user_factory.py` | Cria `CustomUser` com hash PBKDF2 automático |
| **Factory** | `apps/pets/factories/pet_factory.py` | Cria `Pet` com `available=True` por padrão |
| **Singleton** | `patterns/singleton.py` | `AppConfigService` — instância única de log/config |
| **Strategy** | `patterns/strategies/validation_strategy.py` | Algoritmos de validação trocáveis sem alterar o chamador |
| **Strategy** | `patterns/strategies/image_strategy.py` | Estratégia de upload extensível (local → nuvem) |

### Princípios SOLID

- **S** — Cada classe tem uma única responsabilidade (model, repo, service, view separados)
- **O** — Novas estratégias de validação/upload sem modificar código existente
- **L** — Serializers e strategies estendem base sem quebrar comportamento
- **I** — Interfaces enxutas (`validate`, `upload`, `get_upload_path`)
- **D** — Services recebem dependências injetadas (repository, factory, strategy)

---

## Como rodar com uv

### 1. Pré-requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) instalado: `pip install uv`

### 2. Instalar dependências

```bash
cd 16_GET_A_PET_DJANGO
uv sync
```

### 3. Configurar variáveis de ambiente

```bash
copy .env.example .env
# Edite .env se necessário (o default já funciona para desenvolvimento)
```

### 4. Criar e aplicar migrations

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 5. Criar superusuário (opcional)

```bash
uv run python manage.py createsuperuser
```

### 6. Rodar o servidor de desenvolvimento

```bash
uv run python manage.py runserver
```

Acesse: http://localhost:8000

---

## Como rodar os testes

```bash
uv run python manage.py test apps.users.tests apps.pets.tests --verbosity=2
```

Ou com pytest:

```bash
uv run pytest
```

---

## Endpoints da API

### Usuários (`/api/users/`)

| Método | Endpoint | Auth | Descrição |
|--------|----------|------|-----------|
| POST | `/api/users/register/` | Não | Cadastro de novo usuário |
| POST | `/api/users/login/` | Não | Login — retorna tokens JWT |
| GET | `/api/users/checkuser/` | Opcional | Retorna usuário atual |
| POST | `/api/users/token/refresh/` | Não | Renova access token |
| GET | `/api/users/<id>/` | Não | Detalhes públicos do usuário |
| PATCH | `/api/users/<id>/edit/` | Sim | Edição de perfil (somente dono) |

### Pets (`/api/pets/`)

| Método | Endpoint | Auth | Descrição |
|--------|----------|------|-----------|
| GET | `/api/pets/` | Não | Lista todos os pets |
| POST | `/api/pets/` | Sim | Cria novo pet (multipart/form-data) |
| GET | `/api/pets/mypets/` | Sim | Pets do usuário autenticado |
| GET | `/api/pets/myadoptions/` | Sim | Adoções agendadas pelo usuário |
| GET | `/api/pets/<id>/` | Não | Detalhes do pet |
| PATCH | `/api/pets/<id>/` | Sim | Atualiza pet (somente dono) |
| DELETE | `/api/pets/<id>/` | Sim | Remove pet (somente dono) |
| PATCH | `/api/pets/<id>/schedule/` | Sim | Agenda visita |
| PATCH | `/api/pets/<id>/conclude/` | Sim | Conclui adoção (somente dono) |

### Documentação

- Swagger UI: http://localhost:8000/api/docs/
- Admin Django: http://localhost:8000/admin/

### Autenticação

Envie o token no header:
```
Authorization: Bearer <access_token>
```

---

## Deploy (Render)

O projeto inclui `render.yaml` e `Procfile` prontos para deploy no Render com PostgreSQL.

1. Conecte o repositório no [Render](https://render.com)
2. O `render.yaml` provisiona automaticamente o banco PostgreSQL
3. Defina as variáveis de ambiente no painel (ou deixe o `render.yaml` gerar `SECRET_KEY`)

---

## Estrutura do banco de dados

```
CustomUser          Pet                 PetImage
-----------         -------             ----------
id (PK)             id (PK)             id (PK)
name                name                pet_id (FK→Pet)
email (unique)      age                 image
phone               weight
password (hash)     color
image               available
                    owner_id (FK→User)
                    adopter_id (FK→User, nullable)
                    created_at
                    updated_at
```
