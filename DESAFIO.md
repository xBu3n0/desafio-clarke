# Desafio Clarke Energia

SPA de escolha de fornecedor. Os usuários poderão **selecionar o estado (UF)**, informar o seu consumo de energia e visualizar **quais soluções estão disponíveis (GD e/ou Mercado Livre)**, bem como a **economia estimada** e os **fornecedores disponíveis** em cada solução.

---

# Dos Requisitos de Produto:

* O usuário deverá **selecionar o estado (UF)**.

* O usuário deverá informar o seu **consumo mensal de energia**, exemplo: **30000 kWh** (um número fictício > 0).

* Ao informar o consumo e selecionar o estado, o sistema deverá mostrar:

  * Quais soluções estão disponíveis no estado (**GD** e/ou **Mercado Livre**).
  * Quais fornecedores estão disponíveis **em cada solução**.
  * A **economia estimada** que o usuário teria **por solução** (GD e Mercado Livre), considerando o estado selecionado.

* Em um mesmo estado, **vários fornecedores** podem atuar com **GD** ou com **Mercado Livre** (ou ambos).
* Da mesma maneira, uma mesma fornecedora pode atuar em vários estados
* Todos os dados devem ser fictícios

* Cada fornecedor deve ter as seguintes informações:

  * **nome**
  * **logo**
  * **estado de origem**
  * **tipo de solução** (**GD** e/ou **Mercado Livre**)
  * **custo por kWh (por solução)**
  * **número total de clientes**
  * **avaliação média dos clientes**

* O **custo por kWh do fornecedor deve variar por solução**.

  * Exemplo conceitual:

    * GD → `custo_kwh_gd`
    * Mercado Livre → `custo_kwh_ml`

* Para cálculo de economia, você deve assumir um **custo base por kWh por estado** (definido em um mock/seed), e então calcular:

  * `custo_base = consumo_kwh * tarifa_base_kwh(estado)`
  * Para cada fornecedor e solução:

    * `custo_fornecedor = consumo_kwh * custo_kwh_fornecedor(solucao)`
    * `economia = custo_base - custo_fornecedor`
    * (Opcional) `economia_percentual = economia / custo_base`

* O sistema deve apresentar a economia:

  * **Por solução** (ex.: melhor economia encontrada entre os fornecedores daquela solução no estado).
  * **Por fornecedor**, permitindo comparação entre fornecedores da mesma solução.

---

# Requisitos Técnicos:

* O frontend deve ser feito em **React**.

* O backend deve ser feito em **Python** ou **NodeJs**.

---

# Entrega Final

Você deverá enviar um email para `tecnologia@clarke.com.br` e `people@clarke.com.br` com o seguinte título:

**`Desafio Clarke Energia | <Seu Nome>`**

No email, você deve fornecer **2 links**:

* Link para o repositório principal do projeto
  (você deve compartilhar o projeto com os usuários `victorcopque` e `EloisaSM` no GitHub)
* Link para o projeto disponível online
  (recomendamos serviços como **Netlify** ou **Vercel** para hospedar frontend e backend; fique à vontade para usar outras plataformas equivalentes)

---

# Diferenciais

Os itens a seguir **não são obrigatórios**. Lembre-se que o principal diferencial é o desafio ser entregue. Os candidatos terão uma avaliação melhor se:

* A aplicação for integrada com **GraphQL**
* O frontend tiver testes automatizados com **Jest** ou **Cypress**
* O backend tiver testes automatizados
* Os arquivos para que a aplicação funcione via **Docker** estiverem configurados

