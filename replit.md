# Sistema de Agendamento de Passaportes - Polícia Federal

## Visão Geral
Aplicação web desenvolvida para simular o sistema de agendamento de passaportes da Divisão de Passaporte da Polícia Federal do Brasil. O projeto foi criado com HTML/CSS no frontend e Python/Flask no backend.

## Status do Projeto
- **Data de criação**: 01/11/2025
- **Status**: MVP Completo e Funcional
- **Versão**: 1.0

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
   - Cores oficiais (#337ab7)

2. **Formulário de agendamento**
   - Seleção de quantidade de solicitações (1-5)
   - Validação e processamento via Flask

3. **Página de confirmação**
   - Exibe detalhes do agendamento
   - Gera protocolo aleatório único
   - Mostra data/hora do registro
   - Botão para voltar à página inicial

## Tecnologias Utilizadas
- **Backend**: Python 3.11, Flask 3.0.0
- **Frontend**: HTML5, CSS3, Jinja2
- **Fontes**: Google Fonts (Roboto)
- **Ícones**: Font Awesome 5.15.3

## Como Usar
1. A aplicação roda automaticamente na porta 5000
2. Acesse a página inicial para ver o formulário
3. Selecione a quantidade de solicitações (1-5)
4. Clique em "PROSSEGUIR"
5. Veja a confirmação com protocolo gerado

## Configuração
- **Servidor**: Flask Development Server
- **Host**: 0.0.0.0 (todas interfaces)
- **Porta**: 5000
- **Debug**: Ativado

## Próximas Fases (Planejadas)
1. Sistema de autenticação de usuários
2. Banco de dados PostgreSQL para persistência
3. Sistema de pagamento de GRU
4. Painel administrativo
5. Calendário para seleção de datas/horários

## Arquitetura
- **Padrão MVC** com Flask
- **Templates Jinja2** para renderização HTML
- **CSS separado** para manutenibilidade
- **Rotas RESTful** para navegação
