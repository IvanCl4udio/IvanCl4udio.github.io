---
title: "The Holy Grail of Automation: Composite Actions, Reusable Workflows, and GitHub-Wide Standardization"
description: "Combine composite actions and reusable workflows in GitHub Actions with secure dependency versioning and explicit organization governance."
date: 2025-12-10
draft: false
editorialReview: "approved"
language: "en"
translationKey: "reusable-workflows"
originalUrl: "https://medium.com/@ivan.claudio/the-holy-grail-of-automation-composite-actions-reusable-workflows-and-github-wide-0c18824e7a96"
---
![Diagram connecting composite actions to a reusable workflow and repository files.](https://cdn-images-1.medium.com/max/800/1*QSYH35ZlnlYHYy9SwZVZRA.png)

Modern DevOps isn’t just about running pipelines—it’s about building **platforms of automation** that scale.\
Once you have a solid Kubernetes cluster, secure secret management with Vault, ephemeral GitHub Actions runners, and GitOps deployments with ArgoCD, another problem inevitably emerges:

> *Every repository has its own pipeline, slightly different, duplicated, and painful to maintain.*

You update Java in one repo but forget another.\
You fix Docker caching in one place but break it somewhere else.\
Slowly, CI/CD becomes a zoo of inconsistent YAML.

This is the moment to adopt the final evolutionary stage of GitHub automation:

- **Composite Actions** → reusable *steps*
- **Reusable Workflows** → reusable *pipelines*
- **Organization-level `.github`** **repository** → centralized governance and standardization

Together, they turn fragmented automation into a **coherent platform**.

> **Illustrative examples:** `example-org` is a placeholder, not an available organization or dependency. The `push-docker` and `deploy-argocd` actions are interface sketches; their implementations are not supplied here. The latter must authenticate, update the GitOps source, and report reconciliation/health according to your platform. These snippets are not a tested deployment pipeline. `@v1` and the official action major tags below are readable examples, not immutable production pins; replace them with reviewed full commit SHAs and check runner compatibility before execution.

## 1. Composite Actions—Encapsulating Reusable Logic

Composite Actions let you package multiple steps into a single reusable unit.\
They can live:

- in the **same repository** as your application, or
- in a **central automation repository** (ex: `ci-kit`), or
- in the **organization-wide `.github`** **repo**

The `checkout@v4` and `setup-java@v4` references preserve the original example’s release family; they are not claims about the latest releases. Select a supported release from the official [checkout](https://github.com/actions/checkout) and [setup-java](https://github.com/actions/setup-java) repositories, review its changes and runner requirements, and pin the corresponding full commit SHA.

### Example directory (in a repo called `ci-kit`)

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
        cache-dependency-path: ${{ inputs.working-directory }}/pom.xml
    - name: Build with Maven
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: mvn -B clean package
```

### Using it in any workflow

```yaml
- name: Build Java
  uses: example-org/ci-kit/build-java@v1
  with:
    java-version: '21'
```

If the action were local to the repo, you’d call:

```yaml
uses: ./.github/actions/build-java
```

Composite Actions reduce duplication and share behavior across callers that adopt the same revision. A local action requires checkout before its `uses: ./...` step.

## 2. Reusable Workflows—Packaging Entire Pipelines

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

### Consuming this workflow from an app repository

```yaml
name: Application CI/CD
on:
  push:
    branches: [main]
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

If the workflow lived in the **same repo**:

```yaml
uses: ./.github/workflows/build-and-deploy.yml
```

Reusable Workflows allow you to define CI/CD once—and apply it everywhere.

## 3. Before and After—Raw Pipeline vs Standardized Pipeline

### Raw, duplicated pipeline (without reusability)

```yaml
name: Application CI/CD
on:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 21
          cache: maven
      - run: mvn -B clean package
      - env:
          DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
        run: printf '%s' "$DOCKERHUB_TOKEN" | docker login -u ivancl4udio --password-stdin
      - run: docker build -t ivancl4udio/customer-api:${{ github.sha }} .
      - run: |
          docker push ivancl4udio/customer-api:${{ github.sha }}
      - run: |
          # Apply manifest updates
          # Trigger ArgoCD sync
```

This appears in every repo—slightly different each time.\
It’s brittle, hard to maintain, and error-prone.

### Using a reusable workflow

```yaml
name: Application CI/CD
on:
  push:
    branches: [main]
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

Callers share the same CI logic at their selected revision. An improvement reaches SHA-pinned consumers only after they review and update that reference.

This is what platform engineering feels like.

## 4. Organization-Level Standardization with `.github`

GitHub allows organizations to create a special repository named **`.github`**.

Inside it, you can define:

```text
example-org/.github/          # repository
 ├── .github/
 │    ├── workflows/
 │    │    ├── ci-java.yml
 │    │    ├── ci-node.yml
 │    │    └── security-scan.yml
 │    └── CODEOWNERS
 └── workflow-templates/      # optional templates
```

These workflows can be adopted as **official standards**. Hosting them here does not automatically run them in other repositories.

### Example: standard Java CI workflow

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
      - uses: example-org/ci-kit/build-java@v1
      - uses: example-org/ci-kit/push-docker@v1
        with:
          image: ${{ inputs.image }}
          tag: ${{ github.sha }}
        env:
          DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

A repository can simply declare:

```yaml
uses: example-org/.github/.github/workflows/ci-java.yml@v1
```

This is how teams share:

- consistent build steps
- shared security-scan definitions
- unified deployment patterns
- shared tooling and governance

This can be a building block of an **Internal Developer Platform (IDP)**, alongside self-service interfaces, operational ownership, and enforced controls.

## 5. Versioning, Governance, and Evolution

To avoid breaking the world:

- Publish semantic releases (for example, `v1.2.3`) and document compatibility. Major aliases such as `v1` are convenient but mutable. Pin external actions and reusable workflows to a reviewed **full commit SHA** for reproducibility; keep the release version in a comment and update through reviewed dependency changes.
- Avoid breaking changes inside the same major version.
- Document everything inside `README.md` for each composite action and workflow.
- Treat your CI/CD definitions as code with backward compatibility in mind.

This supports controlled evolution; review and test updates before rolling them out across repositories.

## Operational Contracts and Enforcement

A reusable workflow is called at job level; local workflow references have no `@ref` and use the caller’s commit. Local actions are steps and require checkout. The Java composite requires Maven, Bash, a checked-out `pom.xml`, and a runner compatible with the chosen `setup-java` release; the cache path follows `working-directory`. The caller must check out the application before invoking it.

The build/push/deploy sketches assume a Dockerfile compatible with the Maven artifact. `push-docker` must implement registry login with a scoped token, build, and push using its declared `image` and `tag` inputs. The separate deploy job does not inherit files or credentials from build: transfer artifacts explicitly when needed. A commit-SHA image tag aids traceability but remains mutable; use a verified image digest for deployment. The raw example’s commented manifest/sync step performs no deployment.

Pass secrets explicitly, only to jobs that need them. `permissions: contents: read` limits `GITHUB_TOKEN`, not the separate registry or ArgoCD tokens. A reusable workflow cannot elevate the caller’s token permissions. Configure the named environment’s branch restrictions and required approvals separately; the `environment` input alone creates no approval policy. Keep privileged workflows away from untrusted code. GitOps writes need their own reviewed, scoped authentication and concurrency/stale-build safeguards; committing a manifest is distinct from ArgoCD reconciliation and a healthy rollout.

An organization’s `.github` repository is a distribution point. Workflow templates in `workflow-templates/` are copied starting points, while reusable workflows live in `.github/workflows/` and are explicitly called. `CODEOWNERS` applies to the repository containing it; require code-owner review through protections. For enforcement, configure branch protections or rulesets with required checks, and required workflows where supported by the organization’s plan. Restrict bypass permissions and allowed Actions. Reuse alone neither enforces scans nor constitutes a complete IDP.

References: [composite action metadata](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax), [reusable workflow syntax and permissions](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows), [dependency and secret security](https://docs.github.com/en/actions/reference/security/secure-use), [workflow templates](https://docs.github.com/en/actions/how-tos/reuse-automations/create-workflow-templates), [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), and [deployment environments](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments).

## 6. Conclusion

Composite Actions and Reusable Workflows transform GitHub Actions from a collection of pipelines into a **cohesive automation platform**.

This is the moment where:

- YAML duplication decreases
- maintenance scales gracefully
- CI/CD becomes consistent, predictable, and elegant
- new services adopt shared practices through explicit configuration
- your automation evolves like a real product

After securing the cluster, optimizing builds, and automating deployments, this final step completes the journey:

> *Standardization. Reuse. Governance.\
> The Holy Grail of DevOps automation.*

You’re no longer “writing pipelines”.\
You’re **architecting automation**.

This article was originally written in Portuguese and later translated into English to make the content accessible to a broader audience.\
If you prefer to read the original version, it is available here:\
[**https://medium.com/@ivan.claudio/o-santo-graal-composite-actions-workflows-reutilizáveis-e-padronização-em-escala-74cb832e3669**](https://medium.com/@ivan.claudio/o-santo-graal-composite-actions-workflows-reutiliz%C3%A1veis-e-padroniza%C3%A7%C3%A3o-em-escala-74cb832e3669)
