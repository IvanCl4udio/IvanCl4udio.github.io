---
title: "Prompt Engineering for Developers: From Chaos to Control"
description: "A seven-part prompt framework and hybrid workflow for developers, with practical Copilot guidance, explicit constraints, and independent validation."
date: 2025-12-18
draft: false
editorialReview: "approved"
language: "en"
translationKey: "prompt-engineering"
originalUrl: "https://medium.com/@ivan.claudio/prompt-engineering-for-developers-from-chaos-to-control-f0c02475ecf8"
---
![Diagram connecting a central prompt to specifications, configuration, and code.](https://cdn-images-1.medium.com/max/800/1*2tRlHxtSeFR7jHZuupg4WA.png)

There’s a familiar complaint in the world of AI:

> *“I asked the model to do X and it produced something completely wrong. This AI is useless.”*

You’ve probably heard that. You may have said it.\
Often, part of the problem is a vague or underspecified prompt, written with the hope that the model would *guess* the missing details. But even a clear prompt can fail: model limitations, missing context, and tool errors also matter.

Large language models cannot know your unstated intent.\
They operate through patterns, constraints, and probabilities.

A poor prompt invites structured chaos.\
A good prompt gives engineered output a better chance — and still needs review.

This article explains the difference—and more importantly, how you, as a developer, can turn AI into a **consistent, reliable part of your engineering workflow**. Clear prompting can help across: pipelines, refactoring, documentation, debugging, testing, frontend, backend—all of it.

Let’s break down the engineering choices we can actually control.

## What a Prompt Actually Is (and Why Developers Undervalue It)

The biggest misconception in AI is thinking a prompt is “just a message.”\
Something like:

- “Create a workflow?”
- “Refactor this?”
- “Fix this error?”

To the model, that’s equivalent to:

> *“Do something with this. No context. No constraints. Good luck.”*

A prompt is a message that we can treat as a **specification**.

It’s the cognitive equivalent of a well-written RFC or a design document.\
The quality of the output depends directly on the quality of the specification.

Just like no one expects a robust implementation from a sloppy feature ticket, you cannot expect good code from a sloppy prompt.

## The Anatomy of a Bad Prompt

Bad prompts share five symptoms:

1.  **Vague objective**
2.  **Missing context**
3.  **Multiple tasks mixed together**
4.  **No constraints**
5.  **No output format**

Example:

> *“Make an efficient Dockerfile.”*

Efficient… for what?\
A JVM app? Native Quarkus? Node? Python? Multi-stage? Distroless? Alpine? GPU? CPU?

The model tries to guess, and the result disappoints.\
The specification is one place to investigate; the model and its available context can also be part of the problem.

## The Anatomy of an Excellent Prompt

Now compare with this:

> You are a DevOps engineer specialized in container optimization.\
> Generate a multi-stage Dockerfile for a Quarkus 3.24 application running on Java 21.

> **Requirements:**\
> - target a final image < 200 MB; measure it and report if the target is infeasible\
> - use Distroless\
> - declare port 8080 with EXPOSE; enforce network access separately at runtime\
> - no external tools or unnecessary packages

> Output: Dockerfile only, inside a code block.

This prompt defines:

- objective
- role
- context
- constraints
- output format

This is what a prompt looks like when treated as engineering.

## Core Techniques for Controlling AI Like an Engineer

### 1. Role Conditioning

Tell the model who it must impersonate:

- “You are a senior SRE.”
- “You are a strict code reviewer.”
- “Impersonate a cloud architect.”

This gives the model a perspective, vocabulary, and review criteria. It does not establish expertise or prove that a specific internal reasoning mechanism has been activated.

Role guidance defines a review perspective; **context** supplies facts and files; **structured input/output** organizes data; **validation** checks the result with tools and human judgment. One does not replace the others.

### 2. Scaffolding

For complex tasks, avoid requesting everything at once.

Break the interaction into phases:

1.  architecture
2.  file structure
3.  components
4.  integration
5.  optimization
6.  validation

Staging makes intermediate decisions easier to inspect and correct; the benefit depends on the task and model.

### 3. Structured Input

Send clean, isolated sections:

```text
Here is the code:
<block>

Here is the error:
<block>

Here are the requirements:
<list>
```

Chaos in → chaos out.

### 4. Explicit Constraints

Models fill gaps with assumptions.\
If you don’t define the constraints, you get variance.

For example:

- Specific version
- Allowed libraries
- Forbidden libraries
- Company standards
- Complexity limits
- Code style
- Maximum response size

### 5. Output Locking

Request an explicit output format:

- “Reply with **valid YAML only**.”
- “Code only, no explanations.”
- “Return JSON that passes validation.”

A formatting instruction is not a schema guarantee. Parse YAML or JSON, validate its schema and semantics, and test the result before CI/CD use.

### 6. Disciplined Reasoning

Instead of asking for chain-of-thought, use:

> *“Analyze carefully before answering.”*

The wording alone does not guarantee precision. Ask for assumptions, a concise rationale, and verifiable checks rather than hidden chain-of-thought.

### 7. The Impersonate Technique

This is your superpower:

> “Act like an extremely meticulous senior engineer.”

> “Impersonate an experienced software architect.”

> “Impersonate a PR reviewer with an obsessive attention to detail.”

This overlaps with role conditioning. Specify concrete review criteria; the word “impersonate” is not a separate technical mechanism or a guarantee of rigor.

## Anti-Patterns That Break Everything

Avoid:

- changing topics repeatedly
- sending logs, errors, code, and requests mixed together
- asking for multiple unrelated tasks in one prompt
- expecting the model to infer constraints
- emotional, vague language
- assuming the model “knows what you meant”

AI completes patterns.\
It does not read minds.

## Practical Examples: Before & After

### 1. Unit Tests

**Bad:**

> Create tests for this class.

**Good:**

> You are an advanced test engineer. Generate JUnit 5 tests covering valid, invalid, and edge scenarios. Don’t use Mockito where it doesn’t make sense. Deliver only the final test.

### 2. GitHub Actions Workflow

**Bad:**

> Create a CI workflow.

**Good:**

> Create a GitHub Actions workflow using self-hosted ephemeral ARC runners with arc-k8s labels.

> The workflow should:

> - run mvn verify\
> - generate a Docker image\
> - publish to Docker Hub\
> - propose a reviewed manifest update with yq through a pull request\
> - let ArgoCD reconcile the approved Git change

### 3. Legacy Refactor

A good refactor prompt always includes:

- constraints
- compatibility requirements
- performance targets
- risk boundaries
- architectural invariants

## Prompt Engineering for GitHub Copilot (Deep, Practical, Precise)

Copilot supports inline completions, chat, and agent workflows across supported editors and GitHub surfaces. Editor context is useful, but it is not the product’s only context or execution environment. Feature availability depends on the IDE, plan, and organization policies.

### 1. Copilot Understands File Intent

Comments become high-signal instructions:

```text
// Implement service layer with repository injection
```

```text
// Optimize this SQL query for PostgreSQL
```

```text
// Create GitHub Actions pipeline with matrix build
```

Copilot treats them like micro-prompts.

### 2. Prefix Prompts Drive Structure

If you start writing:

```java
public record Customer(
```

Copilot may suggest:

- fields
- validators
- constructors
- patterns consistent with the repo

It’s pattern-aware autocomplete on steroids.

### 3. Comment-First Development

Before writing code:

```text
// HTTP handler with validation, retries, structured logging
```

Copilot can suggest an implementation aligned with the comment. Check behavior, failure handling, and tests before accepting it.

### 4. Repository Context and Agents

The [Copilot Workspace technical preview ended on May 30, 2025](https://githubnext.com/projects/copilot-workspace/). It is a historical reference, not a current feature to enable.

Today, distinguish [agent mode in supported IDEs](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/use-copilot-agents/use-agent-mode) from [Copilot agents working asynchronously on GitHub](https://docs.github.com/en/copilot/concepts/agent-capabilities/about-agents/about-github-copilot-agents). They can help with code changes and reviewable pull requests, but their tools, permissions, and execution environments differ. Neither implies that every file is always read or that the repository trains the underlying model.

Attach relevant files and verify references. Ask for documentation or tests as deliverables, then inspect them like any other proposed change.

### 5. Advanced Settings

#### Preview Channels

Use preview extension releases only when you deliberately want to evaluate changes. Availability varies by editor; preview builds are not a requirement for good prompts and can change behavior.

#### Copilot Chat contextualized to the repo

Ask:

> What are the failure points of this module?\
> List all the places where CustomerRepository is called.\
> Why does this test fail?

#### Model Override

Where model selection is supported, choose among the models available to your plan and organization. Compare them on your task; labels such as “rigorous” or “creative” are not guarantees.

Changing the chat model does not automatically change the inline-completion model; consult [model selection in Copilot Chat](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/chat-with-copilot/change-the-chat-model).

#### Inline Chat

In VS Code, use the configured inline-chat shortcut (typically Ctrl+I on Windows/Linux or Cmd+I on macOS) to ask:

> Simplify this code while maintaining semantics.

### 6. Copilot thrives on small, focused tasks

For inline completion, useful starting points include:

- a comment describing intent,
- the function signature,
- a partial code block,
- and the initial file structure.

Review the proposed completion. Chat and agent tasks may need broader context and multiple iterations.

### 7. A Practical Mini-Framework for Prompts

The framework I use has seven parts. They make intent and acceptance criteria explicit; adapt them to the task rather than treating them as a formula for perfect answers.

#### The 7-Part Framework

1. Objective
2. Context\
3. Role of AI (Impersonate)\
4. Constraints\
5. Output Format\
6. Examples\
7. Validation

Simple. Direct. Powerful.

## Validation and CI/CD Boundaries

The versions in these prompts (Quarkus 3.24, Java 21, React 18) describe the example, not a recommendation to use the latest release. Supply the actual lockfiles, API contracts, and supported versions. The Java record is an intentionally incomplete prefix, and the React example is a specification, not a tested component.

For both workflow prompts, require `permissions: contents: read` by default, reviewed full commit SHAs for external actions, and least-privilege registry credentials supplied through secrets. Keep untrusted pull requests away from publishing credentials and privileged self-hosted runners. Ephemeral ARC runners still need isolation and access controls; `arc-k8s` is an illustrative runner scale-set name, not proof of a configured runner. Verify the container-build runtime and the chosen `yq` implementation/version.

Publish a commit-specific image tag and record the image digest; tags can be overwritten. Propose manifest changes through the protected GitOps review path, handle concurrent/stale builds, and distinguish a Git commit from ArgoCD reconciliation and rollout health. If CLI sync is required, define its scoped credentials and approvals. YAML parsing, workflow linting, tests, and deployment checks are separate tasks: a model self-check cannot claim they ran without tool output. If prerequisites are missing, report them before returning a supposedly final YAML file.

See [GitHub’s prompt guidance](https://docs.github.com/en/copilot/concepts/prompting-and-context/prompt-engineering), [secure workflow guidance](https://docs.github.com/en/actions/reference/security/secure-use), and [deployment environments](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments).

## 🔥 Example Prompt Using the Full Framework (Senior Level)

Imagine you need to generate a GitHub Actions workflow for a Quarkus + Kubernetes + ArgoCD application using ephemeral ARC runners.

The average person would ask for something like:

> Create a CI/CD workflow.

A more useful engineering specification would look like this:

> **Objective:**\
> Create a complete GitHub Actions CI/CD workflow for a Quarkus application deployed via ArgoCD.

> **Context:**\
> App uses Quarkus 3.24 + Java 21. Build runs on ARC ephemeral runners (`arc-k8s`). Images go to Docker Hub. After build, update Kubernetes manifest using `yq` and propose a reviewed GitOps change.

> **Role (Impersonate):**\
> Impersonate a senior DevOps engineer with deep expertise in GitHub Actions and Kubernetes automation.

> **Constraints:**\
> - No deprecated actions\
> - Must use buildx with caching\
> - Trigger only on push to `main`\
> - No experimental syntax\
> - No excessive comments\
> - ArgoCD reconciles approved Git state; CLI sync only if explicitly required

> **Output Format:**\
> Return **only the YAML file**, in a code block.

> **Examples:**\
> Bad example: workflows without caching, without buildx, with raw `docker build`, or bypassing GitOps review.

> **Validation:**\
> Before answering, verify:\
> - YAML is valid\
> - ARC runner prerequisites are listed; report configuration as unverified without environment access\
> - Image tags include commit SHA\
> - Manifest update uses `yq`\
> - Reconciliation and rollout checks are defined; report execution as unverified without tool evidence

This is what a professional prompt looks like.

## 8. The Hybrid Prompt Model: A Real-World Strategy

By this point in the article, you’ve probably realized that prompt engineering isn’t about memorizing ready-made formulas.

Much less about choosing between giant or small prompts.

A practical engineering approach is a hybrid model, which combines:

- broad prompts to align vision
- specific prompts to generate modules
- iterative prompts to refine
- verification prompts to validate

This methodology emerged from practice, especially when generating complete applications, where the model may exhibit:

- transmission interruptions
- partial file loss
- inconsistencies in connected components
- broken imports
- divergence between modules generated at different times

This experience showed something crucial:

Work within the model’s context window and output limits. Keep decisions explicit and version the files; human cognition is only an analogy here.

Let’s break down the hybrid approach.

### 8.1. Large Prompts for Scaffolding and Architecture

Large prompts can generate code, but I prefer to use them first to establish the architecture and acceptance criteria.

They are useful for generating:

- the application map
- the architecture,
- the directories,
- the layers,
- the rules,
- contracts (DTOs, interfaces, models),
- decision patterns,
- style conventions.

It’s like asking an architect to produce:

- the blueprint,
- the layout,
- the structural requirements.

Without this, each module is born with its own logic—and the project becomes a wasteland.

### 8.2. Small Prompts for Modules

After establishing the architecture, you shift gears.

Now the focus is on modularity:

- generate only one React component
- generate only one service function
- create only one hook
- write only the test for that class
- produce only the workflow
- adjust only the Dockerfile
- fix only that error in the console

These smaller prompts:

- maintain focus
- reduce the chance of cuts or truncations
- make variations easier to compare
- make consistency easier to review
- reduce the scope for unwanted modifications to already validated files

This part corresponds to traditional incremental development.

### Example Small Prompt

Once the architecture, scaffolding, and patterns are defined in the large prompt, you move on to working in isolated modules. Here’s a concrete example of how a smaller prompt should be structured—direct, focused, and with a lower risk of truncation.

### Example of a React Component Module Prompt to create a Customer

> You are a frontend developer specializing in React and TypeScript.\
> Create the CreateCustomerForm.tsx component responsible for sending a POST request to /api/v1/customers.

> **Context:**\
> - The project uses Vite, React 18, TypeScript, React Router, and Axios.\
> - The backend follows the Customer model with the attributes: first_name, middle_name, last_name, email, mobile.

> **Requirements:**\
> - Create a controlled form with simple validation of required fields.\
> - Show error messages below each field.\
> - In case of success, redirect the user to /customers.\
> - In case of an API error, display an alert on the page itself.\
> - Minimal styling using only CSS Modules (do not use external libraries).

> - Do not create routes, only the component.

> **Format:**

> Submit only the final CreateCustomerForm.tsx file as a code block.

> **Validation:**

> Before submitting, check:

> - if all imports exist in the project,

> - if the component does not reference anything that has not yet been created,

> - if the API call is consistent with the informed endpoint,

> - and if the TypeScript is correctly typed.

### Why does this prompt work so well?

- It doesn’t try to do everything at once.
- It doesn’t change the architecture or alter already approved files.
- It focuses only on a single module.
- It supplies relevant detail to reduce unsupported assumptions.
- It establishes clear limits and explicit constraints.
- It requires validation, creating a kind of self-check.

That helps catch breakages; compilation, tests, and human review are still required.

### 8.3. Integration Prompt

After each module exists in isolation, you create a prompt that integrates everything:

> You are a senior engineer reviewing the project integration.

> Analyze **only** the already generated files and **do not directly modify any of them**.

> Check:\
> - if all imports point to valid paths\
> - if all referenced components exist\
> - if all routes used in the frontend are defined\
> - if all consumed services exist and use the correct endpoints\
> - if there are inconsistencies in name, typing, or props\
> Deliver:\
> - a list of inconsistencies found\
> - specific suggestions for correction, without rewriting entire files\
> This prompt acts like a human lint.

It’s like structural QA.

### 8.4. Reinforcement Prompt (Senior Review)

Finally, you run the prompt representing the “senior engineer reviewing the work”:

> You are a senior engineer reviewing the project.

> Analyze all the code already generated, but do not rewrite any entire files.

> Look for and list only:\
> - naming inconsistencies\
> - discrepancies in the standards defined in the scaffolding\
> - logic duplications\
> - weak or error-prone sections\
> - inconsistencies between typings\
> - integration risks\
> - points where complexity can be reduced

> Deliver an organized diagnosis, followed by specific suggestions for improvement.

This step can improve the code and produce guidance to include in later prompts or repository instructions. It does not retrain the underlying model or guarantee persistence across sessions.

### 8.5. Why Use This Strategy?

![The Prompts Hybrid Model organizes AI work into four stages: architecture, modules, integration, and review—supporting clarity and consistency in real-world projects.](https://cdn-images-1.medium.com/max/800/1*Zksst9LShVsNaOtpeHfzjw.png)

*The Prompts Hybrid Model organizes AI work into four stages: architecture, modules, integration, and review—supporting clarity and consistency in real-world projects.*

Because AI models:

- have context limitations
- have output limits; the surrounding service or connection can also interrupt a response
- may omit or fail to use relevant context in long interactions
- can mix contexts when the request is too large
- tend to “hallucinate details” when they need to fill in gaps

Overloaded prompts can lose consistency.

Underspecified prompts can lose the wider picture.

Hybrid prompts help balance vision and incremental verification. They are an engineering strategy, not a universal performance result.

## 9. Conclusion—There Is No One-Size-Fits-All Prompt Strategy

Prompt engineering isn’t about memorizing rigid patterns.\
There’s no “ideal prompt size” that works for every case, just as there’s no single architectural pattern that serves all applications.

What exists is context—and the right approach depends on how you integrate AI into your workflow:

- Sometimes a large prompt is the best solution because it defines the vision, patterns, and skeleton of the project.
- Sometimes small prompts help with precision, focus, and stability.
- Sometimes you combine the two—and this is where the hybrid model truly shines.

More important than the prompt size is the clarity of intent:

- explicit objective
- sufficient context
- well-established constraints
- defined format
- final validation

With these elements and independent checks, AI becomes easier to evaluate and integrate into the development process. Its output remains fallible.

This skill doesn’t replace technical knowledge—it complements it. And, when combined with real engineering experience, it can help reduce rework when the generated changes are independently verified.

In the end, prompt engineering isn’t magic.

It’s simply another way to transform intention into structure—like all engineering work.
