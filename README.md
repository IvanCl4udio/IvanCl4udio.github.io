# IvanCl4udio — portfólio e blog

Foundation do site de Ivan Claudio Fernandes, com foco em liderança de Platform Engineering, DevOps e SRE. Requisitos: [PROJECT_BRIEF.md](PROJECT_BRIEF.md); instruções: [AGENTS.md](AGENTS.md).

## Estado

Estrutura bilíngue EN em `/` e PT-BR em `/pt-br/`. As dez páginas institucionais foram aprovadas pelo proprietário e estão com `draft = false` e `editorialReview = "approved"`, elegíveis para o build de produção. Artigos do Medium e demonstrações continuam em draft. Essa liberação local não autoriza deploy. Os textos de Home e About foram aprovados editorialmente e integrados nos dois idiomas, com perfil nativo do Blowfish, headline, bio e descrições SEO. A revisão visual e a publicação continuam pendentes. A configuração `robots = "noindex, nofollow"` e o bloqueio de rastreamento em `layouts/robots.txt` deverão ser revisados antes do lançamento.

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

Fluxo: branch de trabalho → revisão humana → PR → check obrigatório `build` → merge autorizado. O workflow **Validate Hugo** e seu job `build` permanecem inalterados.

### Publicação manual preparada (ainda não executada)

`.github/workflows/deploy.yml` executa somente por `workflow_dispatch` e aceita apenas `main`. Push/merge não dispara esse deploy. O job `package` reutiliza os passos do CI para instalar Hugo com checksum oficial, conferir versões Docker/CI, verificar módulos e gerar produção sem drafts em `public/`. Não usa Jekyll. `scripts/validate-pages-artifact.py` exige as dez páginas institucionais EN/PT-BR, rejeita fontes Markdown/configurações, arquivos ocultos, links simbólicos e demonstrações. Somente `./public` é enviado ao Pages. O job `deploy`, dependente do pacote validado, recebe exclusivamente `pages: write` e `id-token: write`, usa o ambiente `github-pages` e lê a configuração com `enablement: false`. A concorrência global `github-pages` impede deploys simultâneos sem cancelar um deploy em andamento.

Actions oficiais conferidas nas releases: checkout v7.0.1, setup-go v7.0.0, configure-pages v6.0.0, upload-pages-artifact v5.0.0 e deploy-pages v5.0.1. As versões exatas estão fixadas no YAML; a instalação do Hugo segue a verificação SHA-256 já usada no CI.

Diagnóstico local: só existia `ci.yml`, sem build/artefato/deploy Pages. Publicar Markdown é compatível com Pages configurado para uma branch/raiz; a origem remota atual **não foi verificada**. O workflow preparado corrige o caminho de publicação quando a origem for alterada pelo proprietário para GitHub Actions.

**Páginas institucionais aprovadas:** os arquivos abaixo estão com `draft = false` e `editorialReview = "approved"` nos dois idiomas:

| Página | EN | PT-BR |
| --- | --- | --- |
| Home | `content/en/_index.md` | `content/pt-br/_index.md` |
| About | `content/en/about.md` | `content/pt-br/about.md` |
| Articles | `content/en/articles/_index.md` | `content/pt-br/articles/_index.md` |
| Projects | `content/en/projects/_index.md` | `content/pt-br/projects/_index.md` |
| Contact | `content/en/contact.md` | `content/pt-br/contact.md` |

Os quatro artigos importados do Medium e os quatro `foundation-example.md` permanecem draft. Somente as dez páginas institucionais foram liberadas para o build local de produção. `robots = "noindex, nofollow"` e `layouts/robots.txt` com `Disallow: /` permanecem ativos; publicação não implica indexação.

Após autorização separada para cada ação externa:

1. Revisar o diff, autorizar commit/push e abrir PR; aguardar `Validate Hugo / build`. Este preparo não altera o check obrigatório nem as proteções.
2. Conferir a liberação institucional já aprovada, validar novamente a saída e autorizar separadamente o merge em `main`. O deploy continua manual após merge.
3. Em **Settings → Pages → Build and deployment → Source**, selecionar **GitHub Actions**. Não selecionar publicação de uma branch/raiz. Essa mudança pode afetar a publicação antiga; exige autorização.
4. Em **Settings → Environments → github-pages**, restringir deployment a `main` e configurar revisores obrigatórios se disponíveis. `workflow_dispatch` exige ação de alguém com permissão, mas não representa por si só uma segunda aprovação humana.
5. Com autorização de publicação, abrir **Actions → Deploy Hugo to GitHub Pages → Run workflow**, selecionar **main** e executar. O workflow precisa existir na branch padrão para aparecer na interface. Aprovar o ambiente quando solicitado.
6. Conferir os jobs, artefato e URL prevista `https://ivancl4udio.github.io/`, incluindo `/pt-br/` e páginas institucionais. Não há execução remota validada nesta entrega.

O validador impede upload quando falta algum HTML institucional. Após a aprovação das dez páginas, o build de produção e a validação do artefato passam. Para repetir localmente com as ferramentas fixadas: `hugo --minify --environment production --panicOnWarning` e `python3 scripts/validate-pages-artifact.py public`.

Validação local deste preparo: Hugo Extended 0.167.0 e Go 1.25.6 confirmados; produção e prévia passaram sem avisos usando o módulo em cache; `go mod verify` passou. Antes da aprovação institucional, as dez páginas faltavam na produção e o gate rejeitava o pacote, como esperado. Após a liberação aprovada, os dez HTMLs estão presentes e o gate passa. Na prévia, idiomas e 326 referências locais de páginas/assets foram conferidos sem destinos ausentes. Medium/demonstrações e Markdown de origem estão ausentes da produção. Fixtures temporárias confirmaram aceitação de um pacote completo e rejeição de home ausente, Markdown, configuração e symlink. YAML, permissões, igualdade dos passos de produção com o CI e `git diff --check` passaram. `hugo mod get` falhou por DNS no sandbox; a repetição fora dele ficou sem resposta e foi interrompida. Portanto, a consulta online de dependências e o CI remoto não estão validados. Não houve nova revisão visual em navegador ou Lighthouse; templates, CSS e conteúdo não mudaram.

## Verificações da Foundation

Builds locais com e sem drafts e verificação de integridade do módulo devem passar sem avisos. Revisar saída pública, links de idioma e ausência dos drafts. Design, revisão visual desktop/mobile, teclado, Lighthouse e SEO final ficam para as fases 2–3; nenhum resultado dessas verificações é presumido nesta fase.

### Validação do ambiente Docker

Validado em Linux amd64: `make dev`, `make version`, `make build`, configuração Compose, Go 1.25.6, integridade do módulo e ausência das demonstrações draft no build de produção. As homes EN/PT-BR e um draft responderam por HTTP; uma alteração temporária foi reconstruída automaticamente e depois restaurada. O script de live reload estava presente no HTML. Atualização visual em navegador e execução remota do CI ainda não foram verificadas.

### Home Executive Tech

A Home usa `homepage.layout = "executive"`, pelo ponto de extensão nativo do Blowfish, sem modificar o módulo. `layouts/partials/home/executive.html` renderiza o Markdown; os shortcodes `home/hero`, `home/expertise` e `home/section` organizam a composição. Os textos e rótulos traduzidos permanecem em cada `content/<idioma>/_index.md`; as cinco especialidades ficam no front matter `landing.expertise`.

`assets/css/home.css` é carregado somente nas Homes pelo hook `extend-head-uncached.html`. O desenho abstrato em SVG é decorativo e não representa infraestrutura real. Não há novas fontes, serviços externos ou JavaScript. Dark é a aparência inicial; o seletor nativo permite escolher light. Preferências já salvas pelo visitante continuam sendo respeitadas.

O redesenho preservou os drafts e o bloqueio de indexação. Após aprovação posterior, somente as páginas institucionais foram liberadas de draft; o bloqueio de indexação permanece. CTAs apontam para páginas locais existentes e para o LinkedIn confirmado pelo proprietário; artigos e projetos ainda incluem conteúdo de demonstração na prévia com drafts, sem representar cases publicados. Para revisar: `make dev`, abrir ambos os idiomas em desktop e mobile e conferir também a aparência clara.

Refinamento visual: composição de até 1168px úteis no desktop, ilustração de até 500px e textos com largura limitada. Em telas estreitas, cards em coluna única e ilustração de 210px. Os ícones das especialidades são SVG locais em `layouts/partials/home/expertise-icon.html`; cards informativos não recebem foco artificial. O Hero oferece um link de contato configurado em `params.contact.linkedin`: https://www.linkedin.com/in/ivanclaudio/, confirmado pelo proprietário para ambas as versões de idioma. Essa confirmação não autoriza o lançamento do site.

### About / Sobre Executive Tech

As duas páginas `about.md` usam `layout = "about"`, resolvido por `layouts/_default/about.html`. Esse template define somente o bloco principal e preserva o template base, a navegação, o seletor de idioma e o head de SEO do Blowfish. Metadados visuais de artigo, autoria duplicada e paginação não são renderizados. `description`, `translationKey` e o bloqueio de indexação permanecem; após aprovação do proprietário, About está com `draft = false`.

Os textos aprovados continuam integralmente nos arquivos Markdown, sem cópias nos templates. O shortcode `about/hero` recebe o título da introdução; `about/section` recebe `title`, `kind` e `number`. Os tipos são `journey`, `leadership`, `approach` e `sharing`. A primeira frase/parágrafo de `leadership` e `approach` recebe destaque visual; cada parágrafo de `journey` forma um card. A disposição não atribui datas à trajetória. O CTA final utiliza a página de artigos do idioma atual.

O hook `extend-head-uncached.html` carrega os estilos da Home também no About para reutilizar paleta, largura, botões, tipografia e ilustração. `assets/css/about.css` contém apenas ajustes com escopo `.executive-about`; os artigos técnicos não carregam esses estilos. Nenhum módulo do tema foi alterado e não foram adicionadas dependências ou JavaScript.

Prévia com drafts: http://localhost:1313/about/ e http://localhost:1313/pt-br/about/. Revisar ambos os idiomas em 375px, 430px, 1440px e 1920px, nos temas claro e escuro. A revisão visual local não autoriza publicação.

### Articles e Projects — listagens Executive Tech

`layouts/articles/list.html` e `layouts/projects/list.html` são exclusivos das listagens. Os artigos e projetos individuais continuam com os templates do Blowfish. Partials em `layouts/partials/collections/` compartilham Hero, estado vazio e etiquetas; cada tipo de conteúdo tem seu card próprio. A paleta e os componentes vêm de `home.css`; somente as seções carregam `assets/css/collections.css`. Nenhuma alteração visual foi feita em Home ou About.

As introduções editáveis e descrições SEO estão em `content/<idioma>/articles/_index.md` e `content/<idioma>/projects/_index.md`. Rótulos e estados vazios estão em `i18n/en.toml` e `i18n/pt-br.toml`. As quatro seções foram aprovadas pelo proprietário e agora usam `draft = false` e `editorialReview = "approved"`. O build de produção inclui essas listagens com estado vazio enquanto seus artigos e projetos permanecem em draft. Deploy exige autorização separada.

As listagens incluem automaticamente páginas regulares da seção e subseções, ordenadas pela data mais recente. O filtro explícito `Draft = false` exclui demonstrações mesmo na prévia com `--buildDrafts`; páginas futuras também seguem a configuração Hugo `buildFuture = false`. A prévia permite abrir drafts diretamente pela URL, mas não os anuncia nos cards. Não há grupos anuais vazios nem cards de exemplo. Depois da autorização para tornar uma seção pública, ela mostra o estado vazio enquanto não houver itens publicáveis.

Para adicionar conteúdo, use os archetypes existentes:

```bash
hugo new content --kind articles content/en/articles/my-article.md
hugo new content --kind projects content/en/projects/my-project.md
```

Edite o Markdown, `title`, `description`, data editorial real e `tags`. O resumo do card utiliza `description`, com fallback para o resumo do Hugo. Articles mostra data e tempo de leitura apenas quando disponíveis. Nos projetos, os campos opcionais são:

```toml
projectType = "personal"
category = ""
technologies = []
```

Escolha `projectType = "personal"` (projeto pessoal), `"reference"` (arquitetura de referência) ou `"professional"` (case profissional) conforme a natureza real e aprovada do trabalho. `category` é um texto editorial opcional; `technologies` é uma lista de nomes. Ausência desses campos não gera afirmações automáticas. Os rótulos dos três tipos são traduzidos, sem traduzir automaticamente títulos, resumos ou conteúdo.

Para PT-BR, crie o arquivo correspondente em `content/pt-br/` somente quando houver tradução revisada e use a mesma `translationKey` nos dois arquivos. Mantenha `draft = true` até a aprovação humana; após aprovação específica para publicação, `draft = false` torna o item elegível para o card no próximo build. Não remova a proteção das seções ou de indexação por esse motivo.

Validação desta entrega: builds de desenvolvimento e produção, fixtures isoladas em `/tmp` para zero/um/três itens nos dois idiomas (incluindo metadados ausentes, drafts e itens futuros), comparação de regressão com Home/About/artigos e Firefox em 375/430/1440/1920px. As fixtures não foram adicionadas ao workspace nem aprovadas/publicadas. Prévia: `/articles/`, `/projects/`, `/pt-br/articles/` e `/pt-br/projects/`.

### Contact / Contato Executive Tech

`content/en/contact.md` e `content/pt-br/contact.md` usam `layout = "contact"`, com template exclusivo em `layouts/_default/contact.html`. A introdução fica em Markdown e o título do Hero em `contact.headline`. O template não renderiza metadados de artigo, autoria duplicada, badge Draft ou paginação. Os títulos de navegação, `translationKey`, idiomas e URLs permanecem; descrições SEO substituem os placeholders. Após aprovação do proprietário, Contact usa `draft = false` e `editorialReview = "approved"`; o bloqueio de indexação continua ativo.

O card do LinkedIn utiliza a URL já confirmada em `config/_default/params.toml`, `contact.linkedin`. Nome e CTA estão em `[[contact.channels]]` de cada idioma. Para adicionar outro canal aprovado, configure uma nova chave de URL em `params.contact` e acrescente um registro com `key`, `name` e `cta` nas páginas; não há necessidade de alterar o layout. Os canais são renderizados pelo partial `contact/channel.html`. Links abrem em nova aba com `noopener noreferrer`, e o nome acessível informa esse comportamento no idioma ativo.

`home.css` fornece os componentes compartilhados; `assets/css/contact.css` é carregado somente em Contact e usa escopo `.executive-contact`. O SVG decorativo local está em `layouts/partials/contact/connections.html`; não representa uma rede real. Os links secundários são resolvidos com `site.GetPage` para Projects e Articles no idioma ativo. Não foram adicionados formulário, backend, JavaScript ou serviços externos.

Prévia com drafts: http://localhost:1313/contact/ e http://localhost:1313/pt-br/contact/. Validado no Firefox em 375/430/1440/1920px, com revisão clara/escura, foco por teclado e contraste da paleta. Builds de prévia/produção passaram sem avisos; Após a aprovação posterior, Contact está incluído na saída de produção. As páginas já aprovadas foram comparadas à baseline, sem diferenças além de linhas em branco no head. O LinkedIn bloqueou a consulta automatizada ao perfil (status 999); a URL confirmada e os atributos do link foram conferidos no HTML, sem afirmar validação remota do destino.
