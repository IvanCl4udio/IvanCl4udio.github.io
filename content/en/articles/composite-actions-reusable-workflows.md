---
title: "The Holy Grail of Automation: Composite Actions, Reusable Workflows, and GitHub-Wide Standardization"
description: "Composite Actions, Reusable Workflows, and organization-level standardization for reusable CI/CD automation."
date: 2025-12-10
draft: true
editorialReview: "pending"
language: "en"
translationKey: "reusable-workflows"
originalUrl: "https://medium.com/@ivan.claudio/the-holy-grail-of-automation-composite-actions-reusable-workflows-and-github-wide-0c18824e7a96"
---
![Diagram connecting composite actions to a reusable workflow and repository files.](https://cdn-images-1.medium.com/max/800/1*QSYH35ZlnlYHYy9SwZVZRA.png)

Modern DevOps isn’t just about running pipelines — it’s about building **platforms of automation** that scale.  
 Once you have a solid Kubernetes cluster, secure secret management with Vault, ephemeral GitHub Actions runners, and GitOps deployments with ArgoCD, another problem inevitably emerges:

> *Every repository has its own pipeline, slightly different, duplicated, and painful to maintain.*

You update Java in one repo but forget another.  
 You fix Docker caching in one place but break it somewhere else.  
 Slowly, CI/CD becomes a zoo of inconsistent YAML.

This is the moment to adopt the final evolutionary stage of GitHub automation:

- **Composite Actions** → reusable *steps*
- **Reusable Workflows** → reusable *pipelines*
- **Organization-level `.github`** **repository** → centralized governance and standardization

Together, they turn fragmented automation into a **coherent platform**.

## 1. Composite Actions — Encapsulating Reusable Logic

Composite Actions let you package multiple steps into a single reusable unit.  
 They can live:

- in the **same repository** as your application, or
- in a **central automation repository** (ex: `ci-kit`), or
- in the **organization-wide `.github`** **repo**

### Example directory (in a repo called `ci-kit`)

```text
ci-kit/
 └── build-java/
       ├── action.yml
       └── README.md
```

### Example: Java/Maven build composite action

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

### Using it in any workflow

```yaml
- name: Build Java
  uses: lab-safer/ci-kit/build-java@v1
  with:
    java-version: '21'
```

If the action were local to the repo, you’d call:

```yaml
uses: ./.github/actions/build-java
```

Composite Actions eliminate duplication and ensure consistent behavior across your entire ecosystem.

## 2. Reusable Workflows — Packaging Entire Pipelines

If Composite Actions are reusable building blocks, **Reusable Workflows** are entire reusable pipelines.

A workflow becomes reusable when it declares:

```yaml
on:
  workflow_call:
```

and lives inside:

```text
.github/workflows/
```

### Example reusable workflow (`build-and-deploy.yml`)

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

### Consuming this workflow from an app repository

```yaml
jobs:
  pipeline:
    uses: lab-safer/ci-kit/.github/workflows/build-and-deploy.yml@v1
    with:
      app-name: customer-api
      image: ivancl4udio/customer-quarkus-pg-rest-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

If the workflow lived in the **same repo**:

```yaml
uses: ./.github/workflows/build-and-deploy.yml
```

Reusable Workflows allow you to define CI/CD once — and apply it everywhere.

## 3. Before and After — Raw Pipeline vs Standardized Pipeline

### Raw, duplicated pipeline (without reusability)

```yaml
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 21
          cache: maven
      - run: mvn -B clean package
      - run: echo "${{ secrets.DOCKERHUB_TOKEN }}" | docker login -u ivancl4udio --password-stdin
      - run: docker build -t ivancl4udio/customer-api:${{ github.sha }} .
      - run: |
          docker push ivancl4udio/customer-api:${{ github.sha }}
          docker tag ivancl4udio/customer-api:${{ github.sha }} ivancl4udio/customer-api:latest
          docker push ivancl4udio/customer-api:latest
      - run: |
          # Apply manifest updates
          # Trigger ArgoCD sync
```

This appears in every repo — slightly different each time.  
 It’s brittle, hard to maintain, and error-prone.

### Using a reusable workflow

```yaml
jobs:
  pipeline:
    uses: lab-safer/ci-kit/.github/workflows/build-and-deploy.yml@v1
    with:
      app-name: customer-api
      image: ivancl4udio/customer-quarkus-pg-rest-api
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

Now every repo shares the same CI logic, and any improvement is applied once and used everywhere.

This is what platform engineering feels like.

## 4. Organization-Level Standardization with `.github`

GitHub allows organizations to create a special repository named **`.github`**.

Inside it, you can define:

```text
.github/
 ├── workflows/
 │    ├── ci-java.yml
 │    ├── ci-node.yml
 │    └── security-scan.yml
 └── CODEOWNERS
```

These workflows act as **official standards** for the entire organization.

### Example: standard Java CI workflow

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
      - uses: lab-safer/ci-kit/build-java@v1
      - uses: lab-safer/ci-kit/push-docker@v1
        with:
          image: ${{ inputs.image }}
        env:
          DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

A repository can simply declare:

```yaml
uses: lab-safer/.github/.github/workflows/ci-java.yml@v1
```

This is how teams enforce:

- consistent build steps
- mandatory security scans
- unified deployment patterns
- shared tooling and governance

In other words: **a true Internal Developer Platform (IDP)** emerging organically from GitHub Actions.

## 5. Versioning, Governance, and Evolution

To avoid breaking the world:

- Use **semantic tags** (`v1`, `v2`…) for all Actions and Workflows.
- Avoid breaking changes inside the same major version.
- Document everything inside `README.md` for each composite action and workflow.
- Treat your CI/CD definitions as code with backward compatibility in mind.

This allows continuous improvement without fear of breaking dozens of pipelines.

## 6. Conclusion

Composite Actions and Reusable Workflows transform GitHub Actions from a collection of pipelines into a **cohesive automation platform**.

This is the moment where:

- YAML duplication disappears
- maintenance scales gracefully
- CI/CD becomes consistent, predictable, and elegant
- new services inherit best practices automatically
- your automation evolves like a real product

After securing the cluster, optimizing builds, and automating deployments, this final step completes the journey:

> *Standardization. Reuse. Governance.  
>  The Holy Grail of DevOps automation.*

You’re no longer “writing pipelines”.  
You’re **architecting automation**.

This article was originally written in Portuguese and later translated into English to make the content accessible to a broader audience.  
 If you prefer to read the original version, it is available here:  
 [**https://medium.com/@ivan.claudio/o-santo-graal-composite-actions-workflows-reutilizáveis-e-padronização-em-escala-74cb832e3669**](https://medium.com/@ivan.claudio/o-santo-graal-composite-actions-workflows-reutiliz%C3%A1veis-e-padroniza%C3%A7%C3%A3o-em-escala-74cb832e3669)
