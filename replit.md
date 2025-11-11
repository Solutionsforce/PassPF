# Sistema de Agendamento de Passaportes - Polícia Federal

## Visão Geral
Aplicação web desenvolvida para simular o sistema de agendamento de passaportes da Divisão de Passaporte da Polícia Federal do Brasil. O projeto foi criado com HTML/CSS no frontend e Python/Flask no backend, com integração completa de pagamento PIX via Nova Era Pagamentos.

## Status do Projeto
- **Data de criação**: 01/11/2025
- **Última atualização**: 11/11/2025
- **Status**: MVP Completo e Funcional + Integração de Pagamento PIX
- **Versão**: 2.0

## Estrutura do Projeto
```
.
├── app.py                          # Backend Flask com rotas
├── requirements.txt                # Dependências Python
├── templates/
│   ├── base.html                   # Template base com header e navbar
│   ├── index.html                  # Página inicial com formulário
│   └── confirmacao.html            # Página de confirmação
└── static/
    └── css/
        └── style.css               # Estilos CSS
```

## Funcionalidades Implementadas
1. **Interface fiel ao design original** da Polícia Federal
   - Barra de acessibilidade no topo
   - Cabeçalho com logo da PF
   - Navegação responsiva
   - Cores oficiais (#337ab7, #2176bc)
   - Design profissional governamental em português

2. **Fluxo completo de solicitação**
   - Formulário multi-página: Dados Pessoais → Documentos → Dados Complementares
   - Revisão de dados antes da confirmação
   - Geração de protocolo único
   - Detecção automática de estado via CEP
   - 3 unidades fake de atendimento por estado (Poupatempo SP, UAI MG, etc.)
   - Agendamento com seleção de data e horário

3. **Sistema de Pagamento PIX - Nova Era Pagamentos**
   - Integração completa com API Nova Era Pagamentos
   - Geração de código PIX para pagamento de R$ 257,25
   - Produto: "Taxa de Inscrição"
   - Autenticação Basic Auth segura
   - Verificação automática de status do pagamento
   - Webhook para notificações de mudança de status
   - Página de checkout profissional com QR Code

4. **Analytics e Monitoramento**
   - Microsoft Clarity implementado em todas as 10 páginas (ID: tznan6o244)
   - Rastreamento completo de comportamento do usuário
   - Mapas de calor e gravações de sessão

5. **Geração de PDF**
   - Download de protocolo em PDF
   - Formato oficial com dados completos
   - Data/hora em fuso horário de Brasília (America/Sao_Paulo)

## Tecnologias Utilizadas
- **Backend**: Python 3.11, Flask 3.0.0
- **Frontend**: HTML5, CSS3, Jinja2, Tailwind CSS
- **Fontes**: Google Fonts (Roboto)
- **Ícones**: Font Awesome 6.0.0
- **PDF**: ReportLab
- **Timezone**: pytz (America/Sao_Paulo)
- **Pagamentos**: Nova Era Pagamentos API
- **Analytics**: Microsoft Clarity

## Como Usar
1. A aplicação roda automaticamente na porta 5000
2. Acesse a página inicial para ver o formulário
3. Selecione a quantidade de solicitações (1-5)
4. Clique em "PROSSEGUIR"
5. Veja a confirmação com protocolo gerado

## Configuração

### Variáveis de Ambiente Obrigatórias
```bash
SESSION_SECRET=sua_chave_secreta_flask
NOVA_ERA_SECRET_KEY=sk_...
NOVA_ERA_PUBLIC_KEY=pk_...
```

### Servidor
- **Desenvolvimento**: Flask Development Server
- **Produção**: Gunicorn (configurado via Procfile)
- **Host**: 0.0.0.0 (todas interfaces)
- **Porta**: 5000
- **Debug**: Ativado apenas em desenvolvimento

### Deploy Heroku
1. Configure as variáveis de ambiente:
   ```bash
   heroku config:set SESSION_SECRET="sua_chave_segura"
   heroku config:set NOVA_ERA_SECRET_KEY="sk_..."
   heroku config:set NOVA_ERA_PUBLIC_KEY="pk_..."
   ```
2. Deploy: `git push heroku main`

## API Nova Era Pagamentos

### Endpoints Implementados
1. **POST /api/gerar-pix** - Gera código PIX para pagamento
2. **GET /api/verificar-pagamento/<transaction_id>** - Verifica status do pagamento
3. **POST /api/webhook-pagamento** - Recebe notificações da Nova Era

### Formato de Pagamento
- Valor: R$ 257,25 (25725 centavos)
- Produto: "Taxa de Inscrição"
- Método: PIX
- Expiração: 10 minutos

## Microsoft Clarity
- **ID do Projeto**: tznan6o244
- **Cobertura**: Todas as 10 páginas HTML
- **Dados Coletados**: Sessões, cliques, mapas de calor, gravações

## Arquitetura
- **Padrão MVC** com Flask
- **Templates Jinja2** para renderização HTML
- **CSS separado** para manutenibilidade
- **Rotas RESTful** para navegação
