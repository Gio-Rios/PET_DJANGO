# Planejamento Ágil — Get a Pet (Django)

## Definição do MVP

O MVP entrega o ciclo completo de adoção: cadastro de usuário → publicação de pet → agendamento de visita → conclusão da adoção.

---

## Backlog de Produto

| ID  | História de Usuário | Prioridade | Status |
|-----|---------------------|------------|--------|
| US01 | Como usuário, quero me cadastrar com nome, e-mail, telefone e senha para acessar o sistema. | Alta | Feito |
| US02 | Como usuário cadastrado, quero fazer login com e-mail e senha para acessar minha conta. | Alta | Feito |
| US03 | Como usuário logado, quero editar meu perfil (nome, e-mail, telefone, foto, senha). | Alta | Feito |
| US04 | Como tutor, quero cadastrar um pet com nome, idade, peso, cor e fotos. | Alta | Feito |
| US05 | Como visitante, quero ver a lista de todos os pets disponíveis para adoção. | Alta | Feito |
| US06 | Como tutor, quero ver apenas os pets que eu cadastrei. | Média | Feito |
| US07 | Como usuário logado, quero agendar uma visita a um pet de outro tutor. | Alta | Feito |
| US08 | Como tutor, quero ver quem agendou visita no meu pet. | Média | Feito |
| US09 | Como tutor, quero concluir a adoção, marcando o pet como adotado. | Alta | Feito |
| US10 | Como tutor, quero editar os dados do meu pet. | Média | Feito |
| US11 | Como tutor, quero remover meu pet do sistema. | Média | Feito |
| US12 | Como usuário logado, quero ver os pets em que agendei visita. | Baixa | Feito |
| US13 | Como desenvolvedor, quero documentação Swagger em /api/docs/. | Baixa | Feito |
| US14 | Como operador, quero que a aplicação rode em Render com PostgreSQL. | Baixa | Feito |

---

## Regras de Negócio Implementadas

1. **Não pode agendar visita no próprio pet** — validada no `PetService.schedule_visit`.
2. **Não pode agendar o mesmo pet duas vezes** — validada no `PetService.schedule_visit`.
3. **Somente o dono pode editar, remover ou concluir** — validada em `PetService._get_and_authorize`.
4. **Senha com hash PBKDF2** — gerenciada pelo `AbstractUser` do Django + `UserFactory`.
5. **E-mail único** — verificado no `UserService` via `UserRepository.email_in_use`.

---

## Arquitetura em Camadas

```
Request → View (I/O HTTP)
              ↓
          Service (Regras de Negócio)
              ↓
        Repository (Queries ORM)
              ↓
           Model (Entidade SQL)
```

---

## Padrões GoF Aplicados

| Padrão | Localização | Função |
|--------|-------------|--------|
| **Factory** | `apps/users/factories/user_factory.py` | Encapsula criação de `CustomUser` com hash de senha |
| **Factory** | `apps/pets/factories/pet_factory.py` | Encapsula criação de `Pet` com valor padrão `available=True` |
| **Singleton** | `patterns/singleton.py` | `AppConfigService` — instância única de logging/configuração |
| **Strategy** | `patterns/strategies/validation_strategy.py` | Algoritmos de validação intercambiáveis por entidade |
| **Strategy** | `patterns/strategies/image_strategy.py` | Estratégias de upload de imagem (local / extensível para nuvem) |

---

## Sprint 1 (MVP — Semana 1-2)

- [x] Configuração do projeto Django + DRF + uv
- [x] Modelo CustomUser com autenticação JWT
- [x] CRUD de pets com upload de imagens
- [x] Fluxo de adoção (agendar + concluir)

## Sprint 2 (Qualidade — Semana 3-4)

- [x] Padrões GoF documentados e aplicados
- [x] Arquitetura em camadas (models / repos / services / views)
- [x] Templates HTML para todas as telas
- [x] Testes de integração com APITestCase
- [x] Documentação Swagger em /api/docs/
- [x] Deploy config para Render (render.yaml + Procfile)
