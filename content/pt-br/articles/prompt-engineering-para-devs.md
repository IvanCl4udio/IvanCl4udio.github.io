---
title: "Prompt Engineering para Devs: do caos ao controle absoluto"
description: "Como transformar prompts em especificações técnicas e fazer a IA produzir resultados consistentes e confiáveis."
date: 2025-12-16
draft: true
editorialReview: "pending"
language: "pt-br"
translationKey: "prompt-engineering"
originalUrl: "https://medium.com/@ivan.claudio/prompt-engineering-para-devs-do-caos-ao-controle-absoluto-ff3e0aa9964c"
---
![Diagrama com um prompt central conectado a especificações, configurações e código.](https://cdn-images-1.medium.com/max/800/1*2tRlHxtSeFR7jHZuupg4WA.png)

Existe uma reclamação clássica no mundo da IA:

> *“Pedi para o modelo fazer X e ele devolveu uma coisa totalmente errada. Essa IA não presta.”*

Esse tipo de frase virou quase folclore — e sempre escondendo o mesmo detalhe incômodo: o prompt era um rascunho preguiçoso, jogado no chat com a esperança infantil de que a IA *adivinhasse* o resto.

Modelos de linguagem não têm telepatia.  
Eles têm padrões, estatística e rigor.

Um prompt ruim produz caos estruturado.  
Um prompt excelente produz engenharia sólida.

Este artigo existe para mostrar exatamente essa diferença — e, mais importante, para transformar a forma como você trabalha com IA no seu dia a dia como desenvolvedor. Quando você domina essa habilidade, tudo melhora: pipelines, testes, refatorações, arquitetura, documentação, troubleshooting.

Vamos abrir a caixa-preta e entender por que isso acontece.

## O que um prompt realmente é (e por que você o subestima)

A maior ilusão da IA moderna é imaginar que um prompt é apenas uma frase digitada no chat.  
 “Cria um workflow?”  
 “Refatora isso?”  
 “Me ajuda com esse erro?”

Para o modelo, isso equivale a:

> *“Faça alguma coisa com isso aqui. Sem contexto. Sem limites. Deus te abençoe.”*

O prompt, tecnicamente, é uma **especificação**.  
Um *contrato cognitivo* entre você e o modelo.

Assim como ninguém espera um resultado consistente a partir de um *RFC* mal escrito, também não existe boa resposta gerada a partir de um prompt pobre.

## A anatomia do prompt ruim

Prompts ruins seguem padrões repetitivos:

1.  **objetivo vago**
2.  **ausência total de contexto**
3.  **mistura de tarefas**
4.  **nenhuma restrição**
5.  **nenhuma instrução de formato**

Exemplo clássico:

> *“Faz um Dockerfile eficiente?”*

Eficiente… para quê?  
Para JVM? Native image? Node? Python? Multi-stage? Alpine? Distroless?

O modelo tenta adivinhar. E você fica frustrado.

## A anatomia do prompt excelente

Agora observe este:

> Você é um engenheiro DevOps especializado em otimização de imagens. Gere um Dockerfile multi-stage para uma aplicação Quarkus 3.24, usando Java 21. A imagem final deve ter menos de 200MB, usar distroless, expor somente a porta 8080 e não incluir ferramentas externas.

> *Entregue* ***somente o Dockerfile*** *em bloco de código.*

Este prompt define:

- objetivo
- papel da IA
- contexto
- restrições
- formato
- tom

É assim que um prompt vira especificação técnica.

## Técnicas essenciais para controlar a IA como um engenheiro, não como um turista

### 1. Role Conditioning

Dizer ao modelo *quem ele é* molda a cadeia de raciocínio.

“Você é um arquiteto cloud rígido.”

“Você é um SRE experiente revisando incidentes.”

Isso funciona porque ativa padrões internos específicos.

### 2. Scaffolding

Não peça tudo de uma vez.

Peça em camadas:

1.  explique a arquitetura
2.  gere o arquivo
3.  otimize
4.  valide
5.  critique a solução

É como pair programming disciplinado.

### 3. Input formatado como adulto

Envie blocos limpos:

```text
Este é o código:
<bloco>

Este é o erro:
<bloco>

Aqui estão os requisitos:
<lista>
```

Misturar tudo num blob é receita para respostas inconsistentes.

### 4. Restrição explícita

Se você não disser, o modelo assume o “melhor caso possível” — que raramente é o seu.

Exemplos:

- versão específica
- libs permitidas
- libs proibidas
- padrões da empresa
- limites de complexidade
- estilo de código
- tamanho máximo da resposta

### 5. Output Locking

Forçar formato garante previsibilidade:

- “Responda **apenas** com YAML válido.”
- “Entregue apenas o código.”
- “Formato JSON, sem explicações.”

Indispensável em CI/CD e DevOps.

### 6. Raciocínio disciplinado

Em vez de pedir o chain-of-thought completo (desnecessário), use:

> *“Analise cuidadosamente antes de responder.”*

Permite que o modelo raciocine internamente sem vazar conteúdo inútil.

### 7. A técnica de Impersonate

Este é o tempero secreto:

> *“Aja como um engenheiro sênior extremamente criterioso.”  
>  “Impersonate um arquiteto de software experiente.”  
>  “Impersonate um revisor de PR com atenção obsessiva a detalhes.”*

Esse tipo de orientação direciona o padrão de raciocínio, elevando o rigor lógico.

## Anti-padrões que sabotam qualquer resultado

- trocar de assunto três vezes na mesma conversa
- mandar log, screenshot, código e dúvida tudo junto
- pedir múltiplas tarefas sem ordem
- pedir sem contexto
- pedir emocionalmente
- esperar que IA adivinhe constraints implícitas

Modelos não leem sua mente.  
Eles completam padrões.

## Casos práticos para devs: antes/depois

### 1. Testes unitários inteligentes

**Ruim:**

> Crie testes para essa classe.

**Excelente:**

> Você é um engenheiro de testes avançado. Gere testes JUnit 5 cobrindo casos válidos, inválidos e cenários extremos. Não use Mockito onde não faz sentido. Entregue apenas o teste final.

### 2. Workflow GitHub Actions complexo

**Ruim:**

> Cria um workflow de CI.

**Excelente:**

> Gere um workflow GitHub Actions usando self-hosted runners ARC efêmeros com labels `arc-k8s`.

> O workflow deve:  
>  • rodar `mvn verify`  
>  • gerar imagem Docker  
>  • publicar no Docker Hub  
>  • atualizar YAML com `yq` no branch `main`  
>  • instruir o ArgoCD a sincronizar

### 3. Refatorar código legado

Prompt excelente inclui:

- preservar assinatura pública
- reduzir complexidade
- isolar efeitos colaterais
- explicar trade-offs
- manter compatibilidade binária

## Prompt Engineering para GitHub Copilot

Copilot não funciona como ChatGPT.  
Ele opera em **contexto local**, dentro do seu editor — VS Code, JetBrains ou Neovim.

Ele tem poderes que pouca gente usa plenamente. Vamos destrinchar.

### 1. Copilot entende estrutura do arquivo

Comentários inteligentes moldam as sugestões:

```text
// create service layer with repository injection using best practices
```

```text
// build a workflow that runs maven verify and uploads artifacts
```

```text
// optimize this SQL query for PostgreSQL
```

Copilot segue isso como um mapa.

### 2. Copilot responde fortemente ao “prefix prompt”

Se você começar a escrever:

```java
public record Customer(
```

Copilot deduz:

- campos possíveis
- validações comuns
- padrões da sua base de código
- bibliotecas usadas

É autocomplete inteligente esteroidal.

### 3. Comentar antes de programar aumenta a qualidade absurda

```text
// create HTTP handler with JSON validation, timeout, retries and structured logging
```

Você escreve o comentário — o Copilot escreve o código.

### 4. Copilot aprende seu repositório

Com **Copilot Workspace**, ele:

- lê sua base de código
- sugere refatorações
- propõe arquiteturas
- cria PRs completos
- identifica relacionamentos entre arquivos
- sintetiza documentação
- propõe testes
- gera diagramas

É pair programming em esteroides sintéticos.

### 5. Configurações avançadas que dev raramente explora

#### Nightly updates

Receba melhorias antes de irem para o canal estável.

#### Copilot Chat contextualizado ao repo

Pergunte:

> *“Quais são os pontos de falha desse módulo?”  
>  “Liste todos os lugares onde* *`CustomerRepository`* *é chamado.”  
>  “Por que este teste falha?”*

#### Override de modelos

Escolha entre modelo rápido, rigoroso, criativo, analítico.

#### Inline Chat

Use `Ctrl+I` para perguntar:

> *“Simplifique esse código mantendo semântica.”*

### 6. Copilot não gosta de prompts longos — gosta de intenção clara

Copilot performa melhor quando você divide:

- comentário descrevendo intenção
- assinatura da função
- bloco parcial de código
- estrutura inicial do arquivo

Ele completa o resto.

### 7. O mini-framework definitivo para prompts perfeitos

Depois de trabalhar com prompts por muito tempo, fica claro que toda instrução realmente eficaz segue a mesma espinha dorsal.  
 Sete partes simples — mas que, quando usadas juntas, transformam IA em uma ferramenta de precisão cirúrgica.

#### O Framework de 7 Partes

1.  **Objetivo**
2.  **Contexto**
3.  **Papel da IA (Impersonate)**
4.  **Restrições**
5.  **Formato de Saída**
6.  **Exemplos**
7.  **Validação**

Simples. Direto. Poderoso.

### Exemplo de um prompt criado com o framework

Imagine que você precisa gerar um workflow GitHub Actions para uma aplicação Quarkus + Kubernetes + ArgoCD usando runners ARC efêmeros.

A massa pediria algo como:

> Cria um workflow de CI/CD.

Mas um engenheiro de verdade escreveria isto:

#### Prompt :

> **Objetivo:**  
> Gerar um workflow GitHub Actions completo de CI/CD para uma aplicação Quarkus que será construída e implantada em Kubernetes usando ArgoCD.

> **Contexto:**  
> O repositório contém uma aplicação Quarkus 3.24 rodando Java 21. O build deve ocorrer em runners ARC efêmeros executados dentro do meu cluster Kubernetes. As imagens são publicadas no Docker Hub. Após o build, a pipeline deve atualizar o manifesto Kubernetes usando `yq` e fazer o ArgoCD sincronizar a aplicação.

> **Papel (Impersonate):**  
> Impersonate um engenheiro DevOps sênior especializado em GitHub Actions, Kubernetes e ArgoCD. Seja extremamente criterioso com padrões de segurança, organização e consistência.

> **Restrições:**  
> - Não usar ações deprecated.  
> - Usar buildx com cache.  
> - Usar runners com label `arc-k8s`.  
> - Rodar apenas em pushes para `main`.  
> - Não usar sintaxe experimental.  
> - Não incluir comentários extensos.  
> - ArgoCD deve ser acionado via CLI.

> **Formato:**  
> Entregar **somente** o YAML final do workflow, em bloco de código, sem explicações.

> **Exemplo para reforço:**  
> Um exemplo ruim seria workflows sem cache, sem buildx, usando `docker build`, sem atualizar YAML e sem sincronizar o ArgoCD.  
> Quero o oposto disso.

> **Validação:**  
> Antes de entregar, verifique se:  
> - O YAML está válido.  
> - O runner ARC está configurado corretamente.  
> - A imagem tem tag com SHA do commit.  
> - O build usa cache.  
> - Há sincronização correta com o ArgoCD.

Esse prompt é praticamente uma *obra de engenharia*. 😁  
Ele reduz erro, aumenta previsibilidade e gera outputs dignos de produção.

## 8. O Modelo Híbrido de Prompts: Estratégia Real para Projetos Reais

A essa altura do artigo, você já percebe que prompt engineering não é sobre decorar fórmulas prontas.  
Muito menos sobre escolher entre prompts gigantes ou prompts pequenos.

O caminho mais eficiente — e o mais próximo do que um engenheiro realmente faria — é **uma abordagem híbrida**, que combina:

- prompts amplos para alinhar visão
- prompts específicos para gerar módulos
- prompts iterativos para refinar
- prompts de verificação para validar

Essa metodologia surgiu pela prática, especialmente quando geramos aplicações completas , onde o modelo pode apresentar :

- cortes de transmissão
- perda parcial de arquivos
- inconsistências em componentes conectados
- imports quebrados
- divergência entre módulos gerados em momentos diferentes

Essa experiência mostrou algo crucial:  
 **IA funciona muito melhor quando você respeita o limite cognitivo do modelo — assim como respeita o limite cognitivo de qualquer engenheiro humano.**

Vamos destrinchar a abordagem híbrida.

### 8.1. Prompts grandes para scaffolding e arquitetura

Prompts grandes não servem para gerar código final.  
Eles servem para gerar:

- o mapa da aplicação
- a arquitetura
- os diretórios
- as camadas
- as regras
- contratos (DTOs, interfaces, modelos)
- padrões decisórios
- convenções de estilo

É como pedir para um arquiteto produzir:

- a planta
- o layout
- os requisitos estruturais

Sem isso, cada módulo nasce com sua própria lógica — e o projeto vira terreno baldio.

### 8.2. Prompts menores para módulos específicos

Depois de estabelecida a arquitetura, você troca de marchas.  
Agora o foco é modular:

- gerar apenas um componente React
- gerar apenas uma função de serviço
- criar apenas um hook
- escrever apenas o teste daquela classe
- produzir apenas o workflow
- ajustar apenas o Dockerfile
- corrigir somente aquele erro no console

Esses prompts menores:

- mantêm foco
- reduz a chance de cortes ou truncamentos
- diminuem a variância
- garantem consistência
- evitam modificações indesejadas em arquivos já validados

Essa parte corresponde ao desenvolvimento incremental tradicional.

### Exemplo para “Prompts menores para módulos específicos”

Depois que a arquitetura, o scaffolding e os padrões estão definidos no prompt grande, você passa a trabalhar em módulos isolados. Aqui está um exemplo concreto de como um prompt menor deve ser estruturado — direto, focado e sem risco de truncamento.

### Exemplo de um Prompt de módulo — Componente React para criar um Customer

> Você é um desenvolvedor frontend especializado em React e TypeScript.

> Gere o componente **CreateCustomerForm.tsx** responsável por enviar um POST para `/api/v1/customers`.

> **Contexto:**  
>  — O projeto usa Vite, React 18, TypeScript, React Router e Axios.  
>  — O backend segue o modelo Customer com os atributos: `first_name`, `middle_name`, `last_name`, `email`, `mobile`.

> **Requisitos:**  
>  — Criar um formulário controlado com validação simples de campos obrigatórios.  
>  — Mostrar mensagens de erro abaixo de cada campo.  
>  — Em caso de sucesso, redirecionar o usuário para `/customers`.  
>  — Em caso de erro de API, exibir um alerta na própria página.  
>  — Estilização mínima usando apenas CSS Modules (não usar libs externas).  
>  — Não criar rotas, apenas o componente.

> **Formato:**  
>  Entregue **somente** o arquivo final `CreateCustomerForm.tsx` em bloco de código.

> **Validação:**  
>  Antes de entregar, verifique:  
>  — se todos os imports existem no projeto,  
>  — se o componente não referencia nada que ainda não foi criado,  
>  — se a chamada da API está consistente com o endpoint informado,  
>  — e se o TypeScript está tipado corretamente.

### Por que esse prompt funciona tão bem?

- Ele **não tenta fazer tudo de uma vez**.
- Ele não muda arquitetura nem altera arquivos já aprovados.
- Ele foca apenas *em um único módulo*.
- Ele usa detalhes suficientes para o modelo não inventar nada.
- Ele estabelece **limites claros** e **restrições explícitas**.
- Ele exige **validação**, criando uma espécie de autocheck.

É exatamente isso que evita as quebras

### 8.3. Prompts de integração

Depois que cada módulo existe isoladamente, você faz um prompt que integra tudo:

> Você é um engenheiro sênior revisando a integração do projeto.

> Analise **apenas** os arquivos já gerados e **não altere nenhum deles diretamente**.

> Verifique:  
>  — se todos os imports apontam para caminhos válidos  
>  — se todos os componentes referenciados existem  
>  — se todas as rotas usadas no frontend estão definidas  
>  — se todos os serviços consumidos existem e usam os endpoints corretos  
>  — se há inconsistências de nome, tipagem ou props

> Entregue:  
>  — uma lista de inconsistências encontradas  
>  — sugestões pontuais de correção, sem reescrever arquivos inteiros

Esse prompt age como um *lint humano*.

É como um QA estrutural.

### 8.4. Prompts de reforço (Revisão sênior)

Por fim, você executa o prompt que representa o “engenheiro sênior conferindo a obra”:

> Você é um engenheiro sênior revisando o projeto.

> Analise todo o código já gerado, mas **não reescreva nenhum arquivo completo**.

> Procure e liste apenas:  
>  — inconsistências de nomenclatura  
>  — divergências nos padrões definidos no scaffolding  
>  — duplicações de lógica  
>  — trechos frágeis ou propensos a erro  
>  — incoerências entre tipagens  
>  — riscos de integração  
>  — pontos onde a complexidade pode ser reduzida

> Entregue um diagnóstico organizado, seguido de sugestões pontuais de melhoria.

Esse passo não só melhora o código — também educa o modelo para manter consistência nos próximos módulos.

### 8.5. Por que isso funciona melhor do que qualquer outra estratégia?

![O Modelo Híbrido de Prompts organiza o trabalho com IA em quatro etapas: arquitetura, módulos, integração e revisão — garantindo clareza e consistência em projetos reais.](https://cdn-images-1.medium.com/max/800/1*ziNR8N3VubYSJWJjybQyyQ.png)

*O Modelo Híbrido de Prompts organiza o trabalho com IA em quatro etapas: arquitetura, módulos, integração e revisão — garantindo clareza e consistência em projetos reais.*

Porque modelos de IA:

- têm limite de contexto
- têm limite de transmissão
- podem perder estado em prompts longos
- podem misturar contextos quando o pedido é grande demais
- têm tendência a “alucinar detalhes” quando precisam preencher lacunas

Prompts grandes demais → perdem consistência.  
Prompts pequenos demais → perdem visão.

Prompts híbridos → mantêm visão + precisão.

É literalmente a forma como engenheiros humanos trabalham.

## 9. Conclusão — Não existe receita pronta, existe estratégia

Prompt engineering não é sobre decorar padrões rígidos.  
Não existe um “tamanho ideal de prompt” que funcione para todos os casos, assim como não existe um único padrão de arquitetura que sirva para todas as aplicações.

O que existe é **contexto** — e a abordagem certa depende de como você integra IA ao seu fluxo de trabalho:

- Às vezes um prompt grande é a melhor solução, porque define a visão, os padrões e o esqueleto do projeto.
- Às vezes prompts pequenos garantem precisão, foco e estabilidade.
- Às vezes você combina os dois — e é aqui que o modelo híbrido realmente brilha.

Mais importante do que o tamanho do prompt é a **clareza da intenção**:

- objetivo explícito
- contexto suficiente
- restrições bem estabelecidas
- formato definido
- validação final

Com esses elementos, a IA deixa de ser imprevisível e passa a funcionar como uma ferramenta sólida, integrada ao processo de desenvolvimento.

Essa habilidade não substitui conhecimento técnico — complementa.  
E, quando combinada com experiência real de engenharia, permite construir sistemas melhores, mais rápidos e com menos retrabalho.

No fim, prompt engineering não é magia.  
É simplesmente mais uma forma de transformar intenção em estrutura — como todo trabalho de engenharia.
