---
title: "Prompt Engineering para Devs: do caos ao controle"
description: "Framework de sete partes e modelo híbrido de prompts para devs, com orientação sobre Copilot, restrições explícitas e validação independente."
date: 2025-12-16
draft: false
editorialReview: "approved"
language: "pt-br"
translationKey: "prompt-engineering"
originalUrl: "https://medium.com/@ivan.claudio/prompt-engineering-para-devs-do-caos-ao-controle-absoluto-ff3e0aa9964c"
---
![Diagrama com um prompt central conectado a especificações, configurações e código.](https://cdn-images-1.medium.com/max/800/1*2tRlHxtSeFR7jHZuupg4WA.png)

Existe uma reclamação clássica no mundo da IA:

> *“Pedi para o modelo fazer X e ele devolveu uma coisa totalmente errada. Essa IA não presta.”*

Esse tipo de frase virou quase folclore — e muitas vezes esconde um detalhe incômodo: o prompt era vago, jogado no chat com a esperança de que a IA *adivinhasse* o resto. Mas um prompt claro também pode falhar: limitações do modelo, contexto ausente e erros de ferramentas entram nessa conta.

Modelos de linguagem não têm telepatia.\
Eles geram respostas a partir de padrões, contexto e probabilidades; rigor precisa ser verificado.

Um prompt ruim convida ao caos estruturado.\
Um prompt excelente dá uma base melhor para engenharia sólida — e ainda precisa de revisão.

Este artigo existe para mostrar exatamente essa diferença—e, mais importante, para transformar a forma como você trabalha com IA no seu dia a dia como desenvolvedor. Prompts claros podem ajudar em: pipelines, testes, refatorações, arquitetura, documentação, troubleshooting.

Vamos olhar para as decisões de engenharia que podemos controlar.

## O que um prompt realmente é (e por que você o subestima)

A maior ilusão da IA moderna é imaginar que um prompt é apenas uma frase digitada no chat.\
“Cria um workflow?”\
“Refatora isso?”\
“Me ajuda com esse erro?”

Para o modelo, isso equivale a:

> *“Faça alguma coisa com isso aqui. Sem contexto. Sem limites. Deus te abençoe.”*

O prompt, tecnicamente, é uma **especificação**.\
Um *contrato cognitivo* entre você e o modelo.

Assim como ninguém espera um resultado consistente a partir de um *RFC* mal escrito, também não convém depender de um prompt pobre para obter uma boa resposta.

## A anatomia do prompt ruim

Prompts ruins seguem padrões repetitivos:

1.  **objetivo vago**
2.  **ausência total de contexto**
3.  **mistura de tarefas**
4.  **nenhuma restrição**
5.  **nenhuma instrução de formato**

Exemplo clássico:

> *“Faz um Dockerfile eficiente?”*

Eficiente… para quê?\
Para JVM? Native image? Node? Python? Multi-stage? Alpine? Distroless?

O modelo tenta adivinhar. E você fica frustrado.

## A anatomia do prompt excelente

Agora observe este:

> Você é um engenheiro DevOps especializado em otimização de imagens. Gere um Dockerfile multi-stage para uma aplicação Quarkus 3.24, usando Java 21. Busque uma imagem final menor que 200 MB, meça o resultado e informe se a meta for inviável. Use distroless, declare a porta 8080 com EXPOSE e não inclua ferramentas desnecessárias. Controle o acesso de rede separadamente em runtime.

> *Entregue* ***somente o Dockerfile*** *em bloco de código.*

Este prompt define:

- objetivo
- papel da IA
- contexto
- restrições
- formato
- tom

É assim que um prompt vira especificação técnica.

## Técnicas essenciais para controlar a IA como um engenheiro, não como um turista

### 1. Role Conditioning

Dizer ao modelo qual papel adotar orienta a perspectiva, o vocabulário e os critérios da resposta.

“Você é um arquiteto cloud rígido.”

“Você é um SRE experiente revisando incidentes.”

Isso não comprova a ativação de um mecanismo interno específico nem transforma a resposta em parecer de especialista.

A orientação de papel define uma perspectiva de revisão; **contexto** fornece fatos e arquivos; **entrada/saída estruturada** organiza os dados; **validação** confere o resultado com ferramentas e julgamento humano. Uma coisa não substitui a outra.

### 2. Scaffolding

Em tarefas complexas, evite pedir tudo de uma vez.

Peça em camadas:

1.  explique a arquitetura
2.  gere o arquivo
3.  otimize
4.  valide
5.  critique a solução

É como pair programming disciplinado.

### 3. Input formatado como adulto

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

Se você não disser, o modelo pode preencher as lacunas com suposições — que podem não corresponder ao seu cenário.

Exemplos:

- versão específica
- libs permitidas
- libs proibidas
- padrões da empresa
- limites de complexidade
- estilo de código
- tamanho máximo da resposta

### 5. Output Locking

Pedir um formato explícito facilita o processamento:

- “Responda **apenas** com YAML válido.”
- “Entregue apenas o código.”
- “Formato JSON, sem explicações.”

A instrução de formato não garante conformidade. Em CI/CD e DevOps, faça parsing de YAML ou JSON, valide schema e semântica e teste o resultado.

### 6. Raciocínio disciplinado

Em vez de pedir o chain-of-thought completo (desnecessário), use:

> *“Analise cuidadosamente antes de responder.”*

Essa frase, sozinha, não garante precisão. Peça premissas, justificativa concisa e verificações observáveis, em vez de uma cadeia de raciocínio interna.

### 7. A técnica de Impersonate

Este é o tempero secreto:

> *“Aja como um engenheiro sênior extremamente criterioso.”\
> “Impersonate um arquiteto de software experiente.”\
> “Impersonate um revisor de PR com atenção obsessiva a detalhes.”*

Essa orientação se sobrepõe ao Role Conditioning. Defina critérios concretos de revisão: a palavra “Impersonate” não é um mecanismo técnico separado nem garante rigor lógico.

## Anti-padrões que sabotam qualquer resultado

- trocar de assunto três vezes na mesma conversa
- mandar log, screenshot, código e dúvida tudo junto
- pedir múltiplas tarefas sem ordem
- pedir sem contexto
- pedir emocionalmente
- esperar que IA adivinhe constraints implícitas

Modelos não leem sua mente.\
Eles completam padrões.

## Casos práticos para devs: antes/depois

### 1. Testes unitários inteligentes

**Ruim:**

> Crie testes para essa classe.

**Excelente:**

> Você é um engenheiro de testes avançado. Gere testes JUnit 5 cobrindo casos válidos, inválidos e cenários extremos. Não use Mockito onde não faz sentido. Entregue apenas o teste final.

### 2. Workflow GitHub Actions complexo

**Ruim:**

> Cria um workflow de CI.

**Excelente:**

> Gere um workflow GitHub Actions usando self-hosted runners ARC efêmeros com labels `arc-k8s`.

> O workflow deve:\
> - rodar `mvn verify`\
> - gerar imagem Docker\
> - publicar no Docker Hub\
> - propor a atualização do manifesto com `yq` por pull request revisado\
> - deixar o ArgoCD reconciliar a alteração Git aprovada

### 3. Refatorar código legado

Prompt excelente inclui:

- preservar assinatura pública
- reduzir complexidade
- isolar efeitos colaterais
- explicar trade-offs
- manter compatibilidade binária

## Prompt Engineering para GitHub Copilot

Copilot oferece sugestões inline, chat e fluxos com agentes em editores compatíveis e em superfícies do GitHub. O contexto do editor é útil, mas não é seu único contexto ou ambiente de execução. Os recursos dependem do IDE, plano e políticas da organização.

### 1. Copilot entende estrutura do arquivo

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

Copilot pode usar isso como orientação.

### 2. Copilot responde fortemente ao “prefix prompt”

Se você começar a escrever:

```java
public record Customer(
```

Copilot pode sugerir:

- campos possíveis
- validações comuns
- padrões da sua base de código
- bibliotecas usadas

É autocomplete inteligente esteroidal.

### 3. Comentar antes de programar explicita a intenção

```text
// create HTTP handler with JSON validation, timeout, retries and structured logging
```

Você escreve o comentário — o Copilot pode sugerir código. Confira comportamento, tratamento de falhas e testes antes de aceitar.

### 4. Contexto do repositório e agentes

A [prévia técnica do Copilot Workspace terminou em 30 de maio de 2025](https://githubnext.com/projects/copilot-workspace/). É uma referência histórica, não um recurso atual para habilitar.

Hoje, diferencie o [modo agente em IDEs compatíveis](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/use-copilot-agents/use-agent-mode) dos [agentes do Copilot que trabalham de forma assíncrona no GitHub](https://docs.github.com/en/copilot/concepts/agent-capabilities/about-agents/about-github-copilot-agents). Eles podem ajudar com alterações de código e PRs revisáveis, mas ferramentas, permissões e ambientes de execução são diferentes. Isso não significa que todos os arquivos sejam sempre lidos nem que o repositório treine o modelo subjacente.

Anexe os arquivos relevantes e confira as referências. Peça documentação ou testes como entregáveis e revise-os como qualquer outra alteração proposta.

### 5. Configurações avançadas que dev raramente explora

#### Canais de prévia

Use versões de prévia das extensões quando quiser avaliar mudanças deliberadamente. A disponibilidade varia por editor; elas não são requisito para bons prompts e podem alterar o comportamento.

#### Copilot Chat contextualizado ao repo

Pergunte:

> *“Quais são os pontos de falha desse módulo?”\
> “Liste todos os lugares onde `CustomerRepository` é chamado.”\
> “Por que este teste falha?”*

#### Override de modelos

Quando houver seleção de modelos, escolha entre os disponíveis no seu plano e organização. Compare resultados na sua tarefa; “rigoroso” ou “criativo” não são garantias.

Trocar o modelo do chat não muda automaticamente o modelo de sugestões inline; consulte a [seleção de modelos no Copilot Chat](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/chat-with-copilot/change-the-chat-model).

#### Inline Chat

No VS Code, use o atalho configurado para inline chat (normalmente `Ctrl+I` em Windows/Linux ou `Cmd+I` em macOS) para perguntar:

> *“Simplifique esse código mantendo semântica.”*

### 6. Copilot: intenção clara e escopo adequado

Para sugestões inline, pontos de partida úteis incluem:

- comentário descrevendo intenção
- assinatura da função
- bloco parcial de código
- estrutura inicial do arquivo

Revise a sugestão. Tarefas em chat ou com agentes podem precisar de contexto mais amplo e várias iterações.

### 7. Um mini-framework prático para prompts

O framework que uso tem sete partes. Elas explicitam intenção e critérios de aceite; adapte-as à tarefa em vez de tratá-las como fórmula para respostas perfeitas.

#### O Framework de 7 Partes

1.  **Objetivo**
2.  **Contexto**
3.  **Papel da IA (Impersonate)**
4.  **Restrições**
5.  **Formato de Saída**
6.  **Exemplos**
7.  **Validação**

Simples. Direto. Poderoso.

## Validação e limites dos exemplos de CI/CD

As versões dos prompts (Quarkus 3.24, Java 21, React 18) descrevem o exemplo; não são recomendação de release mais recente. Forneça lockfiles, contratos de API e versões suportadas reais. O record Java é um prefixo propositalmente incompleto, e o exemplo React é uma especificação, não um componente testado.

Nos dois prompts de workflow, exija `permissions: contents: read` por padrão, SHAs completos revisados para actions externas e credenciais de registry com privilégio mínimo fornecidas por secrets. Não exponha credenciais de publicação ou runners próprios privilegiados a PRs não confiáveis. Runners ARC efêmeros também precisam de isolamento e controle de acesso; `arc-k8s` é um nome ilustrativo de runner scale set, não evidência de configuração. Confira o runtime de build de containers e a implementação/versão de `yq`.

Publique uma tag por commit e registre o digest da imagem; tags podem ser sobrescritas. Proponha alterações de manifesto pelo fluxo protegido de revisão GitOps, trate concorrência/builds obsoletos e diferencie commit Git de reconciliação do ArgoCD e saúde do rollout. Se sync via CLI for necessário, defina credenciais restritas e aprovações. Parsing YAML, lint de workflow, testes e verificações de deploy são tarefas distintas: um autocheck do modelo não pode afirmar que foram executados sem saída das ferramentas. Se faltarem pré-requisitos, informe-os antes de entregar um YAML supostamente final.

Veja a [orientação de prompts do GitHub](https://docs.github.com/en/copilot/concepts/prompting-and-context/prompt-engineering), as [práticas para workflows seguros](https://docs.github.com/en/actions/reference/security/secure-use) e os [ambientes de implantação](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments).

### Exemplo de um prompt criado com o framework

Imagine que você precisa gerar um workflow GitHub Actions para uma aplicação Quarkus + Kubernetes + ArgoCD usando runners ARC efêmeros.

A massa pediria algo como:

> Cria um workflow de CI/CD.

Uma especificação de engenharia mais útil seria esta:

#### Prompt:

> **Objetivo:**\
> Gerar um workflow GitHub Actions completo de CI/CD para uma aplicação Quarkus que será construída e implantada em Kubernetes usando ArgoCD.

> **Contexto:**\
> O repositório contém uma aplicação Quarkus 3.24 rodando Java 21. O build deve ocorrer em runners ARC efêmeros executados dentro do meu cluster Kubernetes. As imagens são publicadas no Docker Hub. Após o build, a pipeline deve atualizar o manifesto Kubernetes usando `yq` e propor a alteração GitOps para revisão.

> **Papel (Impersonate):**\
> Impersonate um engenheiro DevOps sênior especializado em GitHub Actions, Kubernetes e ArgoCD. Seja extremamente criterioso com padrões de segurança, organização e consistência.

> **Restrições:**\
> - Não usar ações deprecated.\
> - Usar buildx com cache.\
> - Usar runners com label `arc-k8s`.\
> - Rodar apenas em pushes para `main`.\
> - Não usar sintaxe experimental.\
> - Não incluir comentários extensos.\
> - ArgoCD reconcilia o estado Git aprovado; sync via CLI somente se explicitamente necessário.

> **Formato:**\
> Entregar **somente** o YAML final do workflow, em bloco de código, sem explicações.

> **Exemplo para reforço:**\
> Um exemplo ruim seria workflows sem cache, sem buildx, usando `docker build`, sem revisão GitOps ou sem verificação de reconciliação.\
> Quero o oposto disso.

> **Validação:**\
> Antes de entregar, verifique se:\
> - O YAML está válido.\
> - Os pré-requisitos do runner ARC estão listados; sem acesso ao ambiente, a configuração é não verificada.\
> - A imagem tem tag com SHA do commit.\
> - O build usa cache.\
> - Há critérios para reconciliação e saúde do rollout; sem evidência das ferramentas, a execução é não verificada.

Esse prompt é praticamente uma *obra de engenharia*. 😁\
Ele ajuda a reduzir ambiguidades e facilita a revisão. A saída ainda precisa de validação independente antes de chegar à produção.

## 8. O Modelo Híbrido de Prompts: Estratégia Real para Projetos Reais

A essa altura do artigo, você já percebe que prompt engineering não é sobre decorar fórmulas prontas.\
Muito menos sobre escolher entre prompts gigantes ou prompts pequenos.

Uma estratégia prática de engenharia é **uma abordagem híbrida**, que combina:

- prompts amplos para alinhar visão
- prompts específicos para gerar módulos
- prompts iterativos para refinar
- prompts de verificação para validar

Essa metodologia surgiu pela prática, especialmente quando geramos aplicações completas, onde o modelo pode apresentar:

- cortes de transmissão
- perda parcial de arquivos
- inconsistências em componentes conectados
- imports quebrados
- divergência entre módulos gerados em momentos diferentes

Essa experiência mostrou algo crucial:\
**Trabalhe dentro da janela de contexto e dos limites de saída do modelo. Registre decisões e versione os arquivos; cognição humana é apenas uma analogia aqui.**

Vamos destrinchar a abordagem híbrida.

### 8.1. Prompts grandes para scaffolding e arquitetura

Prompts grandes podem gerar código, mas prefiro usá-los primeiro para estabelecer arquitetura e critérios de aceite.\
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

Sem isso, cada módulo nasce com sua própria lógica—e o projeto vira terreno baldio.

### 8.2. Prompts menores para módulos específicos

Depois de estabelecida a arquitetura, você troca de marchas.\
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
- reduzem a chance de cortes ou truncamentos
- facilitam a comparação de variações
- facilitam a revisão de consistência
- reduzem o escopo para modificações indesejadas em arquivos já validados

Essa parte corresponde ao desenvolvimento incremental tradicional.

### Exemplo para “Prompts menores para módulos específicos”

Depois que a arquitetura, o scaffolding e os padrões estão definidos no prompt grande, você passa a trabalhar em módulos isolados. Aqui está um exemplo concreto de como um prompt menor deve ser estruturado—direto, focado e com menor risco de truncamento.

### Exemplo de um Prompt de módulo—Componente React para criar um Customer

> Você é um desenvolvedor frontend especializado em React e TypeScript.

> Gere o componente **CreateCustomerForm.tsx** responsável por enviar um POST para `/api/v1/customers`.

> **Contexto:**\
> - O projeto usa Vite, React 18, TypeScript, React Router e Axios.\
> - O backend segue o modelo Customer com os atributos: `first_name`, `middle_name`, `last_name`, `email`, `mobile`.

> **Requisitos:**\
> - Criar um formulário controlado com validação simples de campos obrigatórios.\
> - Mostrar mensagens de erro abaixo de cada campo.\
> - Em caso de sucesso, redirecionar o usuário para `/customers`.\
> - Em caso de erro de API, exibir um alerta na própria página.\
> - Estilização mínima usando apenas CSS Modules (não usar libs externas).\
> - Não criar rotas, apenas o componente.

> **Formato:**\
> Entregue **somente** o arquivo final `CreateCustomerForm.tsx` em bloco de código.

> **Validação:**\
> Antes de entregar, verifique:\
> - se todos os imports existem no projeto,\
> - se o componente não referencia nada que ainda não foi criado,\
> - se a chamada da API está consistente com o endpoint informado,\
> - e se o TypeScript está tipado corretamente.

### Por que esse prompt funciona tão bem?

- Ele **não tenta fazer tudo de uma vez**.
- Ele não muda arquitetura nem altera arquivos já aprovados.
- Ele foca apenas *em um único módulo*.
- Ele fornece detalhes relevantes para reduzir suposições sem fundamento.
- Ele estabelece **limites claros** e **restrições explícitas**.
- Ele exige **validação**, criando uma espécie de autocheck.

Isso ajuda a detectar quebras; compilação, testes e revisão humana continuam necessários.

### 8.3. Prompts de integração

Depois que cada módulo existe isoladamente, você faz um prompt que integra tudo:

> Você é um engenheiro sênior revisando a integração do projeto.

> Analise **apenas** os arquivos já gerados e **não altere nenhum deles diretamente**.

> Verifique:\
> - se todos os imports apontam para caminhos válidos\
> - se todos os componentes referenciados existem\
> - se todas as rotas usadas no frontend estão definidas\
> - se todos os serviços consumidos existem e usam os endpoints corretos\
> - se há inconsistências de nome, tipagem ou props

> Entregue:\
> - uma lista de inconsistências encontradas\
> - sugestões pontuais de correção, sem reescrever arquivos inteiros

Esse prompt age como um *lint humano*.

É como um QA estrutural.

### 8.4. Prompts de reforço (Revisão sênior)

Por fim, você executa o prompt que representa o “engenheiro sênior conferindo a obra”:

> Você é um engenheiro sênior revisando o projeto.

> Analise todo o código já gerado, mas **não reescreva nenhum arquivo completo**.

> Procure e liste apenas:\
> - inconsistências de nomenclatura\
> - divergências nos padrões definidos no scaffolding\
> - duplicações de lógica\
> - trechos frágeis ou propensos a erro\
> - incoerências entre tipagens\
> - riscos de integração\
> - pontos onde a complexidade pode ser reduzida

> Entregue um diagnóstico organizado, seguido de sugestões pontuais de melhoria.

Esse passo pode melhorar o código e produzir orientações para prompts posteriores ou instruções do repositório. Não retreina o modelo nem garante persistência entre sessões.

### 8.5. Por que usar essa estratégia?

![O Modelo Híbrido de Prompts organiza o trabalho com IA em quatro etapas: arquitetura, módulos, integração e revisão—favorecendo clareza e consistência em projetos reais.](https://cdn-images-1.medium.com/max/800/1*ziNR8N3VubYSJWJjybQyyQ.png)

*O Modelo Híbrido de Prompts organiza o trabalho com IA em quatro etapas: arquitetura, módulos, integração e revisão—favorecendo clareza e consistência em projetos reais.*

Porque modelos de IA:

- têm limite de contexto
- têm limites de saída; o serviço ou a conexão também podem interromper uma resposta
- podem omitir ou deixar de usar contexto relevante em interações longas
- podem misturar contextos quando o pedido é grande demais
- têm tendência a “alucinar detalhes” quando precisam preencher lacunas

Prompts sobrecarregados podem perder consistência.\
Prompts sem contexto suficiente podem perder visão.

Prompts híbridos ajudam a equilibrar visão e verificação incremental. É uma estratégia de engenharia, não um resultado universal de performance.

## 9. Conclusão—Não existe receita pronta, existe estratégia

Prompt engineering não é sobre decorar padrões rígidos.\
Não existe um “tamanho ideal de prompt” que funcione para todos os casos, assim como não existe um único padrão de arquitetura que sirva para todas as aplicações.

O que existe é **contexto**—e a abordagem certa depende de como você integra IA ao seu fluxo de trabalho:

- Às vezes um prompt grande é a melhor solução, porque define a visão, os padrões e o esqueleto do projeto.
- Às vezes prompts pequenos ajudam na precisão, no foco e na estabilidade.
- Às vezes você combina os dois—e é aqui que o modelo híbrido realmente brilha.

Mais importante do que o tamanho do prompt é a **clareza da intenção**:

- objetivo explícito
- contexto suficiente
- restrições bem estabelecidas
- formato definido
- validação final

Com esses elementos e verificações independentes, fica mais fácil avaliar e integrar a IA ao desenvolvimento. As respostas continuam sujeitas a erro.

Essa habilidade não substitui conhecimento técnico—complementa.\
E, quando combinada com experiência real de engenharia, pode ajudar a reduzir retrabalho quando as alterações geradas são verificadas de forma independente.

No fim, prompt engineering não é magia.\
É simplesmente mais uma forma de transformar intenção em estrutura—como todo trabalho de engenharia.
