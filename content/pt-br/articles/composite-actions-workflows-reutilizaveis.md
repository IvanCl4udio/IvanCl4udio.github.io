---
title: "O Santo Graal: composite actions, workflows reutilizáveis e padronização em escala"
description: "Como combinar composite actions e workflows reutilizáveis no GitHub Actions, com versionamento seguro e governança organizacional explícita."
date: 2025-12-09
draft: false
editorialReview: "approved"
language: "pt-br"
translationKey: "reusable-workflows"
originalUrl: "https://medium.com/@ivan.claudio/o-santo-graal-composite-actions-workflows-reutiliz%C3%A1veis-e-padroniza%C3%A7%C3%A3o-em-escala-74cb832e3669"
---
![Automação que escala: quando pipelines viram blocos reutilizáveis.](https://cdn-images-1.medium.com/max/800/1*QSYH35ZlnlYHYy9SwZVZRA.png)

*Automação que escala: quando pipelines viram blocos reutilizáveis.*

> **Exemplos ilustrativos:** `example-org` é um placeholder, não uma organização ou dependência disponível. As actions `push-docker` e `deploy-argocd` são esboços de interfaces; suas implementações não são fornecidas aqui. A segunda precisa autenticar, atualizar a fonte GitOps e reportar reconciliação/saúde conforme a plataforma. Os trechos não são uma pipeline de deploy testada. `@v1` e as tags major das actions oficiais abaixo facilitam a leitura; em produção, substitua por SHAs completos revisados e confira a compatibilidade dos runners antes de executar.

## 1) Introdução

Depois de ter o cluster Kubernetes, o Vault, os runners efêmeros e o pipeline GitOps com ArgoCD funcionando, surge o próximo problema “de gente grande”:

> *Tudo funciona, mas cada repositório tem* ***o seu*** *YAML de pipeline, com muita coisa repetida, levemente diferente e difícil de manter.*

Você atualiza a versão do Java em um repo, esquece no outro. Ajusta o login do Docker em um, quebra o cache em outro. A automação começa a virar um zoológico de YAML.

É aí que entram:

- **Composite actions** → empacotam *passos* reutilizáveis.
- **Workflows reutilizáveis** → empacotam *pipelines inteiras* reutilizáveis.

E ambos podem morar:

- no **mesmo repositório** da aplicação,
- em um **repositório central de CI** (ex.: `ci-kit`),
- ou em um **repositório `.github`** **da organização**, virando o “guia de estilo” oficial das pipelines.

## 2) Composite actions: empacotando passos reutilizáveis

As referências `checkout@v4` e `setup-java@v4` preservam a família de releases do exemplo original; não indicam a release mais recente. Selecione uma release suportada nos repositórios oficiais de [checkout](https://github.com/actions/checkout) e [setup-java](https://github.com/actions/setup-java), revise alterações e requisitos do runner e fixe o SHA completo correspondente.

### 2.1. Onde elas vivem

Uma composite action é definida por um arquivo `action.yml` dentro de um diretório qualquer do repositório.

Você pode:

- criar no **mesmo repo** da aplicação, por exemplo:\
   `.github/actions/build-java/action.yml`
- ou em um repo central, por exemplo:\
   `ci-kit/build-java/action.yml`

Chamadas:

- **Local (mesmo repo)**—caminho relativo:

```yaml
- name: Build Java
  uses: ./.github/actions/build-java
```

- **Outro repositório**—caminho `owner/repo/path@ref`:

```yaml
- name: Build Java
  uses: example-org/ci-kit/build-java@v1
```

Obs.: para usar uma action local (`./...`), você precisa ter feito `actions/checkout` antes, porque o código da action vem do próprio repositório.

### 2.2. Exemplo: composite action de build Java/Maven

Estrutura do repo `ci-kit`:

```text
ci-kit/
 └── build-java/
      ├── action.yml
      └── README.md
```

`build-java/action.yml`:

```yaml
name: Build Java Project
description: Builds a Java application using Maven and caches dependencies.
inputs:
  java-version:
    description: 'Java version to use'
    default: '21'
  working-directory:
    description: 'Directory containing the pom.xml'
    default: '.'
runs:
  using: "composite"
  steps:
    - name: Set up Java
      uses: actions/setup-java@v4
      with:
        distribution: temurin
        java-version: ${{ inputs.java-version }}
        cache: maven
        cache-dependency-path: ${{ inputs.working-directory }}/pom.xml
    - name: Build with Maven
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: mvn -B clean package
```

Uso em qualquer workflow:

```yaml
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - name: Build Java
        # se estivesse no próprio repo: uses: ./.github/actions/build-java
        uses: example-org/ci-kit/build-java@v1
        with:
          java-version: '21'
          working-directory: '.'
```

Você centraliza Java + Maven + cache num único lugar. Se amanhã quiser trocar a versão do Java, faz isso **uma vez** na action e atualiza as referências fixadas nos consumidores após revisão.

## 3) Workflows reutilizáveis: empacotando pipelines inteiras

### 3.1. Conceito

Enquanto a composite action é usada dentro de um `step`, o **workflow reutilizável** é chamado direto em `jobs.<job_id>.uses`.

Regras básicas:

a\) O workflow reutilizável precisa estar em `.github/workflows/<arquivo>.yml`.

b\) Ele precisa ter `on: workflow_call`.

c\) Ele pode ser chamado:

- por **caminho relativo** se estiver no mesmo repo, ou
- via `owner/repo/.github/workflows/arquivo.yml@ref` se estiver em outro repo.

### 3.2. Exemplo de workflow reutilizável de build + push + deploy

No repo `example-org/ci-kit`:

`.github/workflows/build-and-deploy.yml`:

```yaml
name: Build and Deploy Workflow
on:
  workflow_call:
    inputs:
      app-name:
        required: true
        type: string
      image:
        required: true
        type: string
      environment:
        required: false
        type: string
        default: dev
    secrets:
      DOCKERHUB_TOKEN:
        required: true
      ARGOCD_TOKEN:
        required: true
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - name: Build Java
        uses: example-org/ci-kit/build-java@v1
      - name: Push Docker image
        uses: example-org/ci-kit/push-docker@v1
        with:
          image: ${{ inputs.image }}
          tag: ${{ github.sha }}
        env:
          DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
  deploy:
    if: github.ref == 'refs/heads/main'
    environment: ${{ inputs.environment }}
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ArgoCD
        uses: example-org/ci-kit/deploy-argocd@v1
        with:
          app-name: ${{ inputs.app-name }}
          environment: ${{ inputs.environment }}
          image: ${{ inputs.image }}
          tag: ${{ github.sha }}
        env:
          ARGOCD_TOKEN: ${{ secrets.ARGOCD_TOKEN }}
```

Uso em um repositório de aplicação (`customer-quarkus-pg-rest-api`), chamando esse workflow do repo `ci-kit`:

```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
permissions:
  contents: read
jobs:
  pipeline:
    uses: example-org/ci-kit/.github/workflows/build-and-deploy.yml@v1
    with:
      app-name: customer-api
      image: ivancl4udio/customer-quarkus-pg-rest-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
      ARGOCD_TOKEN: ${{ secrets.ARGOCD_TOKEN }}
```

Se o workflow reutilizável estivesse **no mesmo repo da aplicação**, bastaria:

`.github/workflows/build-and-deploy.yml` no próprio repo, e chamar assim:

```yaml
permissions:
  contents: read
jobs:
  pipeline:
    uses: ./.github/workflows/build-and-deploy.yml
    with:
      app-name: customer-api
      image: ivancl4udio/customer-quarkus-pg-rest-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

Ou seja:

- outro repo → `org/repo/.github/workflows/arquivo.yml@ref`
- mesmo repo → `./.github/workflows/arquivo.yml` (sem `@ref`)

## 4) Antes e depois: pipeline “crua” vs pipeline padronizada

### 4.1. Pipeline sem reutilização (YAML “cru” em cada repo)

```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
permissions:
  contents: read
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false
      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: maven
      - name: Build with Maven
        run: mvn -B clean package
      - name: Log in to Docker Hub
        env:
          DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
        run: printf '%s' "$DOCKERHUB_TOKEN" | docker login -u ivancl4udio --password-stdin
      - name: Build image
        run: docker build -t ivancl4udio/customer-quarkus-pg-rest-api:${{ github.sha }} .
      - name: Push image
        run: |
          docker push ivancl4udio/customer-quarkus-pg-rest-api:${{ github.sha }}
      - name: Update manifests and sync with ArgoCD
        run: |
          # yq para atualizar tag
          # commit em repo de manifests
          # chamada para argocd sync
```

Agora imagina isso levemente modificado em 5–10 repositórios. Manutenção vira castigo.

### 4.2. Mesma lógica usando workflow reutilizável

No repo da aplicação:

```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
permissions:
  contents: read
jobs:
  pipeline:
    uses: example-org/ci-kit/.github/workflows/build-and-deploy.yml@v1
    with:
      app-name: customer-api
      image: ivancl4udio/customer-quarkus-pg-rest-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
      ARGOCD_TOKEN: ${{ secrets.ARGOCD_TOKEN }}
```

Diferenças:

- O YAML da app fica **curto e legível**.
- Toda a lógica de build/push/deploy está centralizada.
- O repositório da aplicação mostra *intenção*, não implementação.
- Fica óbvio: “este serviço usa o padrão `build-and-deploy` da organização”.

## 5) Padronização via repositório `.github` da organização

GitHub permite um repositório especial chamado **`.github`** na organização.\
Ele geralmente guarda templates e arquivos de comunidade, mas também pode hospedar **workflows reutilizáveis oficiais** da org.

Exemplo:

Org: `lab-safer`\
Repo: `example-org/.github`

Estrutura:

```text
example-org/.github/          # repositório
 ├── .github/
 │    ├── workflows/
 │    │    ├── ci-java.yml
 │    │    ├── ci-node.yml
 │    │    └── security-scan.yml
 │    └── CODEOWNERS
 └── workflow-templates/      # templates opcionais
```

`ci-java.yml` (workflow reutilizável padrão para serviços Java):

```yaml
name: Java CI Standard
on:
  workflow_call:
    inputs:
      image:
        required: true
        type: string
      app-name:
        required: true
        type: string
    secrets:
      DOCKERHUB_TOKEN:
        required: true
permissions:
  contents: read
jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - name: Build Java
        uses: example-org/ci-kit/build-java@v1
      - name: Push Docker
        uses: example-org/ci-kit/push-docker@v1
        with:
          image: ${{ inputs.image }}
          tag: ${{ github.sha }}
        env:
          DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

Qualquer repo da organização pode usar:

```yaml
permissions:
  contents: read
jobs:
  ci:
    uses: example-org/.github/.github/workflows/ci-java.yml@v1
    with:
      image: ivancl4udio/customer-quarkus-pg-rest-api
      app-name: customer-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

Sim, fica esse “duplo `.github`” mesmo:

- primeiro `.github` é o **nome do repo** (`example-org/.github`),
- o segundo `.github/workflows/...` é o **diretório** onde os workflows ficam.

O efeito prático:

- você define **padrões organizacionais** reais,
- oferece um fluxo mínimo compartilhado (build, testes, scan etc.) aos serviços que o adotam,
- centraliza a evolução da esteira.

## 6) Versionamento, governança e evolução

Para não transformar isso em outro tipo de caos, algumas boas práticas ajudam:

a) Publicar releases semânticas, como `v1.2.3`, com contrato de compatibilidade. Aliases como `v1` são convenientes, mas mutáveis. Fixe actions e workflows externos em **SHA completo de commit** revisado, com a versão em comentário; atualize as referências por mudanças revisadas de dependências.

b\) Mudanças compatíveis → mesma major (`v1.1`, `v1.2`)

c\) Quebras de contrato → nova major (`v2`).

d\) Documentar cada composite action e cada workflow com `README.md`, descrevendo:

- inputs,
- secrets necessários,
- exemplos de uso,
- limitações.

A partir daí:

- Pequenos ajustes compatíveis podem ser publicados em `v1.x`, com testes e revisão antes da adoção.
- Mudanças grandes geram uma nova família (`v2`), e os repositórios migram quando fizer sentido.

## Contratos operacionais e enforcement

Um workflow reutilizável é chamado no nível de job; referências locais de workflow não têm `@ref` e usam o commit do chamador. Actions locais são steps e exigem checkout. A composite Java exige Maven, Bash, um `pom.xml` no checkout e runner compatível com a release escolhida de `setup-java`; o caminho do cache acompanha `working-directory`. O chamador precisa fazer checkout da aplicação antes de invocá-la.

Os esboços de build/push/deploy pressupõem um Dockerfile compatível com o artefato Maven. `push-docker` precisa implementar login no registry com token restrito, build e push usando os inputs declarados `image` e `tag`. O job de deploy não herda arquivos ou credenciais do build: transfira artefatos explicitamente quando necessário. A tag com SHA do commit ajuda na rastreabilidade, mas continua mutável; use digest verificado da imagem no deploy. O step comentado de manifesto/sync do exemplo cru não executa deploy.

Passe secrets explicitamente, apenas aos jobs que precisam deles. `permissions: contents: read` limita o `GITHUB_TOKEN`, não os tokens separados de registry ou ArgoCD. O workflow reutilizável não pode elevar as permissões do token do chamador. Configure separadamente restrições de branch e aprovações do ambiente nomeado; o input `environment`, sozinho, não cria política de aprovação. Não exponha workflows privilegiados a código não confiável. Escritas GitOps exigem autenticação própria, revisada e restrita, com controle de concorrência/builds obsoletos; commit de manifesto é diferente de reconciliação do ArgoCD e rollout saudável.

O repositório `.github` da organização é um ponto de distribuição. Templates em `workflow-templates/` são pontos de partida copiados; workflows reutilizáveis ficam em `.github/workflows/` e são chamados explicitamente. `CODEOWNERS` vale para o repositório que o contém; exija revisão dos responsáveis por meio de proteções. Para enforcement, configure proteção de branch ou rulesets com checks obrigatórios, e workflows obrigatórios quando o plano da organização permitir. Restrinja bypass e Actions permitidas. Reutilização, sozinha, não obriga scans nem constitui uma IDP completa.

Referências: [metadados de composite actions](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax), [sintaxe e permissões de workflows reutilizáveis](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows), [segurança de dependências e segredos](https://docs.github.com/en/actions/reference/security/secure-use), [templates de workflow](https://docs.github.com/en/actions/how-tos/reuse-automations/create-workflow-templates), [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) e [ambientes de implantação](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments).

## 7) Conclusão

Composite actions e workflows reutilizáveis são a fronteira entre:

- **“Tenho várias pipelines rodando”**\
   e
- **“Tenho uma plataforma de automação padronizada que evolui como um produto”**.

Você sai do modo “copiar e colar YAML” e entra no modo “definir contratos de automação”.

No nosso cenário—homelab + Kubernetes + Vault + runners efêmeros + ArgoCD—essa camada fecha o arco:

- Infra definida,
- Segredos protegidos,
- Execução isolada,
- Deploy automatizado,
- E agora: **automação padronizada em escala**, com um repo `.github` e um `ci-kit` sustentando tudo.

É aqui que você deixa de ser apenas usuário de pipeline e assume o papel de **arquiteto de automação**.
