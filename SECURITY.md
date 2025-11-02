# 🔒 Guia de Segurança

## Variáveis de Ambiente

Este projeto utiliza variáveis de ambiente para proteger informações sensíveis. **NUNCA** commite chaves de API ou tokens no Git.

### Variáveis Necessárias

#### 1. SESSION_SECRET
- **Descrição:** Chave secreta para criptografia de sessões Flask
- **Como gerar:** 
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- **Exemplo:** `a1b2c3d4e5f6...` (64 caracteres hexadecimais)

#### 2. FOURM_PAYMENTS_API_TOKEN
- **Descrição:** Token de autenticação da API 4M Payments
- **Onde obter:** Painel da 4M Payments (https://app.4mpagamentos.com)
- **Formato:** String alfanumérica fornecida pela 4M

### Configuração no Heroku

```bash
# Definir variáveis
heroku config:set SESSION_SECRET="sua_chave_aqui"
heroku config:set FOURM_PAYMENTS_API_TOKEN="seu_token_aqui"

# Verificar variáveis configuradas
heroku config

# Remover uma variável (se necessário)
heroku config:unset NOME_VARIAVEL
```

### Desenvolvimento Local

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```

2. Edite `.env` com suas chaves **reais**

3. **IMPORTANTE:** O arquivo `.env` está no `.gitignore` e **nunca** será commitado

### Boas Práticas

✅ **FAÇA:**
- Use variáveis de ambiente para todas as chaves
- Gere chaves diferentes para desenvolvimento e produção
- Mantenha `.env` no `.gitignore`
- Rotacione chaves periodicamente
- Use o arquivo `.env.example` como documentação

❌ **NÃO FAÇA:**
- Commitar chaves no código
- Compartilhar chaves em chat/email
- Usar a mesma chave em dev e produção
- Deixar chaves hardcoded no código
- Compartilhar o arquivo `.env`

### Verificação de Segurança

Antes de fazer commit, verifique:

```bash
# Verificar se há chaves expostas
git diff | grep -i "api.*key\|token\|secret"

# Listar arquivos que serão commitados
git status

# Verificar .gitignore
cat .gitignore | grep -E "\.env|secret|key"
```

### APIs Utilizadas

#### 4M Payments API
- **Endpoint:** `https://app.4mpagamentos.com/api/v1`
- **Autenticação:** Bearer Token
- **Documentação:** https://app.4mpagamentos.com/docs

**Endpoints usados:**
- `POST /pix` - Gerar pagamento PIX
- `GET /pix/{transaction_id}` - Verificar status do pagamento

### Auditoria

Comandos úteis para auditar segurança:

```bash
# Verificar variáveis de ambiente configuradas
heroku config --app nome-da-app

# Ver logs em busca de exposição
heroku logs --tail | grep -i "token\|secret\|key"

# Verificar commits recentes
git log --oneline -10
```

### Checklist de Deploy

Antes de fazer deploy:

- [ ] Todas as chaves em variáveis de ambiente
- [ ] `.env` no `.gitignore`
- [ ] Sem chaves hardcoded no código
- [ ] `.env.example` atualizado
- [ ] Variáveis configuradas no Heroku
- [ ] Documentação de segurança lida

---

**Lembre-se:** Segurança é responsabilidade de todos! 🔐
