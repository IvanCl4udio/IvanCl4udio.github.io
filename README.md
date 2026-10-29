# IvanCl4udio — portfólio e blog

Foundation do site de Ivan Claudio Fernandes, com foco em liderança de Platform Engineering, DevOps e SRE. Requisitos: [PROJECT_BRIEF.md](PROJECT_BRIEF.md); instruções: [AGENTS.md](AGENTS.md).

## Estado

Estrutura bilíngue EN em `/` e PT-BR em `/pt-br/`, sem publicação. Todo conteúdo inicial está em draft, inclusive páginas institucionais. Portanto, o build de produção ainda não oferece uma home pública. A revisão visual e a aprovação dos textos pertencem à próxima fase. A configuração `robots = "noindex, nofollow"` deverá ser revisada antes do lançamento.

URL pretendida: https://ivancl4udio.github.io/. Pages não foi ativado nesta fase. A branch local encontrada era `master`; o alvo de integração é `main`, sem migração realizada.

## Ferramentas fixadas

- Hugo **Extended 0.167.0**.
- Blowfish **v3.9.0**, via Hugo Modules; `go.mod` e `go.sum` versionados.
- Go **1.25.6**, versão usada localmente e no CI.

O módulo do tema declara compatibilidade com Hugo Extended 0.164.0–0.167.0. Hugo 0.169.0 foi descartado por gerar aviso de incompatibilidade. Atualizar versões deliberadamente e validar local/CI juntos. Não editar o módulo de terceiros.

## Prévia com Docker Compose

Pré-requisitos: Docker Engine ou Docker Desktop em execução, Docker Compose v2 ou superior e Make. Hugo e Go não precisam estar instalados no host.

```bash
make dev
```

A primeira execução baixa a imagem base, Hugo e o módulo Blowfish; precisa de rede. Abra:

- EN: http://localhost:1313/
- PT-BR: http://localhost:1313/pt-br/

O servidor inclui drafts e faz live reload ao salvar arquivos. Use `Ctrl+C` para interromper e `make down` para remover o serviço, preservando os caches. A porta é exposta somente no loopback do host. A prévia não publica o site.

```bash
make version  # Hugo Extended 0.167.0
make build    # build de produção, sem drafts; saída no volume /cache/public
make down
```

O código é montado somente para leitura no container. Cache do Hugo, módulos Go, recursos gerados e build de produção ficam no volume Docker `hugo-cache`; não são gravados como root no workspace. A imagem contém Go 1.25.6, Git e Hugo Extended 0.167.0, com SHA-256 conferido contra o arquivo oficial da release. Suporta hosts Linux amd64/arm64 e Docker Desktop compatível. A base Go também está fixada por digest. O CI confere o alinhamento das versões entre o workflow e `Dockerfile.dev`; ao atualizar Go, atualize também o digest da imagem base deliberadamente.

Se alterações não forem detectadas pelo Docker Desktop, pare a prévia e execute:

```bash
docker compose run --rm --service-ports hugo server --bind=0.0.0.0 --port=1313 --baseURL=http://localhost:1313/ --buildDrafts --disableFastRender --renderToMemory --noBuildLock --poll=700ms
```

Se a porta 1313 estiver ocupada, encerre o processo que a utiliza antes de iniciar. Erros de acesso ao daemon devem ser resolvidos conforme a configuração local do Docker; o Makefile não usa sudo. Mudanças em dependências ou na imagem podem exigir reiniciar `make dev`.

### Alternativa com ferramentas no PATH

Com as mesmas versões de Hugo Extended e Go instaladas pelo proprietário:

```bash
hugo version
hugo mod get
go mod verify
hugo --minify --environment production --panicOnWarning
hugo server --disableFastRender --buildDrafts
```

`--buildDrafts` serve apenas à prévia. `public/`, `resources/` e caches locais não devem ser versionados.

## Criar e revisar conteúdo

```bash
hugo new content --kind articles content/en/articles/my-article.md
hugo new content --kind articles content/pt-br/articles/meu-artigo.md
hugo new content --kind projects content/en/projects/my-case.md
```

Sem Hugo no PATH, crie conteúdo pelo container usando, por exemplo:

```bash
docker compose run --rm --user "$(id -u):$(id -g)" --volume "$PWD:/site:rw" --env HUGO_CACHEDIR=/tmp/hugo --env GOMODCACHE=/tmp/go-mod --env GOCACHE=/tmp/go-build hugo new content --kind articles content/en/articles/my-article.md
```

Os archetypes incluem título, descrição, data, tags, idioma, `draft` e `editorialReview`. A data criada automaticamente deve ser revisada como data editorial, sem representar um evento profissional. Defina a mesma `translationKey` nas traduções correspondentes; não crie tradução vazia. Mantenha o idioma correto em cada arquivo.

Antes de remover `draft`, revisar os fatos, referências, resultados autorizados, licença dos ativos e ambas as versões quando existirem. Registrar `editorialReview = "approved"` após revisão humana. Esse campo registra o processo editorial; `draft` controla a exclusão do build. Projetos conceituais devem ser identificados explicitamente. Rascunhos versionados também ficam públicos quando o repositório é público.

Os arquivos `foundation-example.md` são demonstrações, não relatos profissionais. Não publicá-los. Páginas institucionais devem ter conteúdo aprovado nos dois idiomas antes do lançamento.

## CI e publicação

`.github/workflows/ci.yml` valida dependências, build de produção, exclusão das demonstrações draft e build de prévia. Usa ações oficiais com versões fixadas e somente `contents: read`. Não publica artefatos nem faz deploy. Sua execução remota ainda não foi validada; exige push autorizado.

Fluxo previsto: branch de trabalho → revisão humana → PR → checks → merge autorizado. Nenhum workflow de deploy ou `CNAME` foi criado. Preparar Pages é uma fase posterior; ativação, push, merge e deploy exigem autorização específica. Quando o workflow de produção estiver habilitado, push/merge em `main` poderá publicar automaticamente.

## Verificações da Foundation

Builds locais com e sem drafts e verificação de integridade do módulo devem passar sem avisos. Revisar saída pública, links de idioma e ausência dos drafts. Design, revisão visual desktop/mobile, teclado, Lighthouse e SEO final ficam para as fases 2–3; nenhum resultado dessas verificações é presumido nesta fase.

### Validação do ambiente Docker

Validado em Linux amd64: `make dev`, `make version`, `make build`, configuração Compose, Go 1.25.6, integridade do módulo e ausência das demonstrações draft no build de produção. As homes EN/PT-BR e um draft responderam por HTTP; uma alteração temporária foi reconstruída automaticamente e depois restaurada. O script de live reload estava presente no HTML. Atualização visual em navegador e execução remota do CI ainda não foram verificadas.
