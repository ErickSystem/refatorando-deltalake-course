# Hotel Booking – Visão Hierárquica de Domínios, Áreas, Times e Data Products

- [Data Mesh: Designing Data Products](https://www.datamesh-architecture.com/data-product-canvas)

---

## Domínio 1: Reservas e Acomodações
Responsável pela gestão das reservas, disponibilidade de quartos e administração de serviços adicionais.

### Departamentos
1. **Gestão de Reservas**  
   - Foca em todos os dados relacionados à criação, atualização e cancelamento de reservas.  
   - Integra-se a canais de venda e marketing.  
   - Monitora disponibilidade e status das reservas (confirmadas, pendentes, canceladas).

### Times

#### Time: Reservas
- **Responsabilidades**:
  - Definir modelos de dados para reservas e acompanhar a evolução dos processos de reserva.
  - Garantir a qualidade e consistência das informações de check-in/check-out.
  - Criar e evoluir Data Products relacionados à ocupação (por exemplo, Painel de Ocupação em Tempo Real).
  - Integrar-se com sistemas externos (marketing, vendas) para sincronizar status de reservas.

### Data Product 1: Painel de Ocupação em Tempo Real
- **Objetivo**:  
  Fornecer uma visão atualizada da disponibilidade e ocupação dos quartos, permitindo decisões de negócio mais ágeis sobre promoções e tarifas.
- **Principais Dados**:  
  - Status das reservas (confirmada, cancelada, pendente)  
  - Tipo de acomodação (standard, luxo, suíte)  
  - Datas de check-in e check-out  
  - Taxa de ocupação por hotel/unidade  

---

## Domínio 2: Pagamentos e Faturamento
Responsável por todas as transações financeiras, emissão de faturas e controle de cobranças.

### Departamentos
1. **Transações Financeiras**  
   - Abrange pagamentos (cartão de crédito, débito, PayPal etc.) e reembolsos.  
   - Foca em segurança financeira, prevenção a fraudes e conformidade com normas (PCI-DSS).  
   - Fornece dados para relatórios de fluxo de caixa e projeções financeiras.

### Times

#### Time: Financeiro
- **Responsabilidades**:
  - Conduzir e monitorar o ciclo de pagamentos, reembolsos e estornos.
  - Manter regras de segurança e compliance para garantir a integridade dos dados financeiros.
  - Criar e manter Data Products para análise de transações (ex.: Histórico de Transações).
  - Fornecer APIs para integração com outros domínios (ex.: Reservas e Acomodações).

### Data Product 2: Histórico de Transações e Faturamento
- **Objetivo**:  
  Consolidar informações de pagamentos, valores faturados, status das cobranças e datas de emissão de faturas, oferecendo uma visão ampla e histórica do fluxo financeiro.
- **Principais Dados**:  
  - ID de transação, valor, método de pagamento  
  - Status da transação (autorizado, negado, pendente)  
  - Data de emissão e vencimento de faturas  
  - Dados de cobrança (multas, taxas de serviço)

---
