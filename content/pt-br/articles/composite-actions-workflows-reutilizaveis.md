---
title: "O Santo Graal: composite actions, workflows reutilizáveis e padronização em escala"
description: "Depois de ter o cluster Kubernetes, o Vault, os runners efêmeros e o pipeline GitOps com ArgoCD funcionando, surge o próximo problema “de gente grande”:"
date: 2025-12-09
draft: true
editorialReview: "pending"
language: "pt-br"
translationKey: "reusable-workflows"
originalUrl: "https://medium.com/@ivan.claudio/o-santo-graal-composite-actions-workflows-reutiliz%C3%A1veis-e-padroniza%C3%A7%C3%A3o-em-escala-74cb832e3669"
---
![Automação que escala: quando pipelines viram blocos reutilizáveis.](https://cdn-images-1.medium.com/max/800/1*QSYH35ZlnlYHYy9SwZVZRA.png)

*Automação que escala: quando pipelines viram blocos reutilizáveis.*

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
- ou em um **repositório `.github`** **da organização**, virando o “guia de estilo” oficial das pipelines.

## 2) Composite actions: empacotando passos reutilizáveis

### 2.1. Onde elas vivem

Uma composite action é definida por um arquivo `action.yml` dentro de um diretório qualquer do repositório.

Você pode:

- criar no **mesmo repo** da aplicação, por exemplo:  
   `.github/actions/build-java/action.yml`
- ou em um repo central, por exemplo:  
   `ci-kit/build-java/action.yml`

Chamadas:

- **Local (mesmo repo)** — caminho relativo:

```yaml
- name: Build Java   
  uses: ./.github/actions/build-java
```

- **Outro repositório** — caminho `owner/repo/path@ref`:

```yaml
- name: Build Java   
  uses: lab-safer/ci-kit/build-java@v1
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
    - name: Build with Maven
      working-directory: ${{ inputs.working-directory }}
      run: mvn -B clean package
```

Uso em qualquer workflow:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Java
        # se estivesse no próprio repo: uses: ./.github/actions/build-java
        uses: lab-safer/ci-kit/build-java@v1
        with:
          java-version: '21'
          working-directory: '.'
```

Você centraliza Java + Maven + cache num único lugar. Se amanhã quiser trocar a versão do Java, faz isso **uma vez** na action.

## 3) Workflows reutilizáveis: empacotando pipelines inteiras

### 3.1. Conceito

Enquanto a composite action é usada dentro de um `step`, o **workflow reutilizável** é chamado direto em `jobs.<job_id>.uses`.

Regras básicas:

a\) O workflow reutilizável precisa estar em `.github/workflows/<arquivo>.yml`.

b\) Ele precisa ter `on: workflow_call`.

c\) Ele pode ser chamado:

- por **caminho relativo** se estiver no mesmo repo, ou
- via `owner/repo/.github/workflows/arquivo.yml@ref` se estiver em outro repo.

### 3.2. Exemplo de workflow reutilizável de build + push + deploy

No repo `lab-safer/ci-kit`:

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
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Java
        uses: lab-safer/ci-kit/build-java@v1
      - name: Push Docker image
        uses: lab-safer/ci-kit/push-docker@v1
        with:
          image: ${{ inputs.image }}
        env:
          DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ArgoCD
        uses: lab-safer/ci-kit/deploy-argocd@v1
        with:
          app-name: ${{ inputs.app-name }}
          environment: ${{ inputs.environment }}
```

Uso em um repositório de aplicação (`customer-quarkus-pg-rest-api`), chamando esse workflow do repo `ci-kit`:

```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
jobs:
  pipeline:
    uses: lab-safer/ci-kit/.github/workflows/build-and-deploy.yml@v1
    with:
      app-name: customer-api
      image: ivancl4udio/customer-quarkus-pg-rest-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

Se o workflow reutilizável estivesse **no mesmo repo da aplicação**, bastaria:

`.github/workflows/build-and-deploy.yml` no próprio repo, e chamar assim:

```yaml
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
- mesmo repo → `./.github/workflows/arquivo.yml` (sem `@ref`)

## 4) Antes e depois: pipeline “crua” vs pipeline padronizada

### 4.1. Pipeline sem reutilização (YAML “cru” em cada repo)

```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: maven
      - name: Build with Maven
        run: mvn -B clean package
      - name: Log in to Docker Hub
        run: echo "${{ secrets.DOCKERHUB_TOKEN }}" | docker login -u ivancl4udio --password-stdin
      - name: Build image
        run: docker build -t ivancl4udio/customer-quarkus-pg-rest-api:${{ github.sha }} .
      - name: Push image
        run: |
          docker push ivancl4udio/customer-quarkus-pg-rest-api:${{ github.sha }}
          docker tag ivancl4udio/customer-quarkus-pg-rest-api:${{ github.sha }} ivancl4udio/customer-quarkus-pg-rest-api:latest
          docker push ivancl4udio/customer-quarkus-pg-rest-api:latest
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
jobs:
  pipeline:
    uses: lab-safer/ci-kit/.github/workflows/build-and-deploy.yml@v1
    with:
      app-name: customer-api
      image: ivancl4udio/customer-quarkus-pg-rest-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

Diferenças:

- O YAML da app fica **curto e legível**.
- Toda a lógica de build/push/deploy está centralizada.
- O repositório da aplicação mostra *intenção*, não implementação.
- Fica óbvio: “este serviço usa o padrão `build-and-deploy` da organização”.

## 5) Padronização via repositório `.github` da organização

GitHub permite um repositório especial chamado **`.github`** na organização.  
 Ele geralmente guarda templates e arquivos de comunidade, mas também pode hospedar **workflows reutilizáveis oficiais** da org.

Exemplo:

Org: `lab-safer`  
 Repo: `lab-safer/.github`

Estrutura:

```text
.github/
 ├── workflows/
 │    ├── ci-java.yml
 │    ├── ci-node.yml
 │    └── security-scan.yml
 └── CODEOWNERS
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
jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Java
        uses: lab-safer/ci-kit/build-java@v1
      - name: Push Docker
        uses: lab-safer/ci-kit/push-docker@v1
        with:
          image: ${{ inputs.image }}
        env:
          DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

Qualquer repo da organização pode usar:

```yaml
jobs:
  ci:
    uses: lab-safer/.github/.github/workflows/ci-java.yml@v1
    with:
      image: ivancl4udio/customer-quarkus-pg-rest-api
      app-name: customer-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

Sim, fica esse “duplo `.github`” mesmo:

- primeiro `.github` é o **nome do repo** (`lab-safer/.github`),
- o segundo `.github/workflows/...` é o **diretório** onde os workflows ficam.

O efeito prático:

- você define **padrões organizacionais** reais,
- força que todos os serviços passem pelo mesmo fluxo mínimo (build, testes, scan, etc.),
- centraliza a evolução da esteira.

## 6) Versionamento, governança e evolução

Para não transformar isso em outro tipo de caos, algumas boas práticas ajudam:

a\) Versionar tudo com tags: `v1`, `v2` etc.

b\) Mudanças compatíveis → mesma major (`v1.1`, `v1.2`)

c\) Quebras de contrato → nova major (`v2`).

d\) Documentar cada composite action e cada workflow com `README.md`, descrevendo:

- inputs,
- secrets necessários,
- exemplos de uso,
- limitações.

A partir daí:

- Pequenos ajustes podem ser aplicados sem medo em `v1.x`.
- Mudanças grandes geram uma nova família (`v2`), e os repositórios migram quando fizer sentido.

## 7) Conclusão

Composite actions e workflows reutilizáveis são a fronteira entre:

- **“Tenho várias pipelines rodando”**  
   e
- **“Tenho uma plataforma de automação padronizada que evolui como um produto”**.

Você sai do modo “copiar e colar YAML” e entra no modo “definir contratos de automação”.

No nosso cenário — homelab + Kubernetes + Vault + runners efêmeros + ArgoCD — essa camada fecha o arco:

- Infra definida,
- Segredos protegidos,
- Execução isolada,
- Deploy automatizado,
- E agora: **automação padronizada em escala**, com um repo `.github` e um `ci-kit` sustentando tudo.

É aqui que você deixa de ser apenas usuário de pipeline e assume o papel de **arquiteto de automação**.
