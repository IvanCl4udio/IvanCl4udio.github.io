# Migração Medium — lote 01

Integração local em `content/medium-import-batch-01`, em 02/11/2026. Sem commit, push, PR ou publicação. Nenhuma configuração remota foi consultada ou alterada.

## Arquivos integrados

| Arquivo em content/ | Data original | translationKey | Blocos de código |
| --- | --- | --- | --- |
| en/articles/prompt-engineering-for-developers.md | 2025-12-18 | prompt-engineering | 6 |
| pt-br/articles/prompt-engineering-para-devs.md | 2025-12-16 | prompt-engineering | 6 |
| en/articles/composite-actions-reusable-workflows.md | 2025-12-10 | reusable-workflows | 14 |
| pt-br/articles/composite-actions-workflows-reutilizaveis.md | 2025-12-09 | reusable-workflows | 13 |

Todos mantêm `draft: true`, `editorialReview: pending`, datas e `originalUrl` de proveniência. Idioma explícito adicionado conforme os diretórios existentes. A autoria usa a configuração existente de Ivan Claudio Fernandes no Blowfish; nenhuma biografia foi adicionada ou alterada.

Não foram alterados layouts, CSS, configuração, navegação ou páginas existentes. A alteração prévia em `.gitignore` foi preservada. Somente os quatro artigos foram copiados. Após as validações, a pasta temporária `.medium-import/` foi removida conforme solicitado, incluindo os cinco drafts não integrados; os originais externos ao repositório não foram acessados nem alterados.

## Ajustes de conversão

- Hierarquia de títulos H2/H3/H4 para distinguir seções e subseções sem reescrever seu texto.
- Correção de delimitadores de ênfase malformados nos exemplos de prompts e de escapes que impediam listas Markdown no EN.
- Rótulos de blocos corrigidos: árvores de diretórios e comentários/instruções são `text`; chamadas `uses:` são `yaml`. Conteúdo e versões dos exemplos preservados.
- Indentação do passo `actions/setup-java@v4` corrigida no exemplo EN de pipeline crua. Nenhum comando foi modernizado ou executado.
- Título EN truncado de Composite Actions adaptado para “The Holy Grail of Automation: Composite Actions, Reusable Workflows, and GitHub-Wide Standardization”; descrição truncada substituída por resumo do assunto. Redação ainda sujeita à revisão editorial.
- Textos alternativos genéricos das ilustrações iniciais substituídos por descrições do conteúdo visual inspecionado. URLs, legendas existentes e imagens preservadas.
- `originalUrl` não foi usado para configurar canonical: o tema continua gerando canonical próprio do site.

## Revisão editorial e técnica pendente

### Composite Actions / Reusable Workflows — ambos os idiomas

- O exemplo de composite action tem `run` sem `shell`: revisar contrato de execução antes de publicar. Preservado como original histórico.
- Confirmar autorização e natureza pública das referências `lab-safer`, `ci-kit`, `customer-api`, `ivancl4udio/customer-quarkus-pg-rest-api` e suas associações. Não houve acesso a esses repositórios ou sistemas. Os nomes não são credenciais, mas podem identificar infraestrutura ou organização.
- Ações `push-docker` e `deploy-argocd` são referenciadas sem implementação no artigo. Exemplos não constituem pipeline completo validado; revisar credenciais, permissões, autenticação, checkout e relação entre imagem construída e implantada.
- Revisar uso de tags mutáveis (`@v1`, `@v4`, `latest`), permissões mínimas e passagem de secrets. Foram encontradas apenas expressões `${{ secrets.DOCKERHUB_TOKEN }}`, sem valores de tokens, chaves privadas ou endpoints internos identificados nesta inspeção.
- Revisar afirmações de que hospedar workflows em `.github` força padrões organizacionais ou aplica automaticamente atualizações a todos os repositórios. Distinguir reuso voluntário de mecanismos de enforcement.
- Preservadas as diferenças entre EN/PT-BR, inclusive 14 versus 13 blocos: não se fabricou equivalência textual.

### Prompt Engineering — ambos os idiomas

- Rever tom categórico sobre previsibilidade, raciocínio, limites e qualidade de modelos; preservar texto histórico até aprovação de alterações.
- A afirmação EN “Most developers use ~10% of its potential” exige evidência ou revisão explícita.
- Revisar atualidade de Copilot Workspace, opções de modelos, nightly updates e comportamento dos editores. Nenhuma funcionalidade atual foi atestada nesta migração.
- Quarkus 3.24, Java 21, React 18 e exemplos de ARC/yq/ArgoCD preservados. Não foram executados nem modernizados; revisar compatibilidade, limites do alvo de 200MB, políticas de push para `main` e sincronização via CLI.
- Fragmento Java é intencionalmente incompleto no exemplo de prefix prompt. A frase PT “É exatamente isso que evita as quebras” e a qualidade da tradução EN também merecem revisão editorial; não foi inventada continuação.

### Imagens e links externos

Quatro imagens distintas do CDN Medium responderam HTTP 200 em 02/11/2026 e foram inspecionadas visualmente. Não foram observados endereços internos ou segredos nas ilustrações. Permanecem remotas, com seis ocorrências nos quatro artigos. Confirmar licença/autoria e decidir armazenamento local/otimização antes de publicar: os arquivos atuais têm aproximadamente 0,87–1,36 MB cada e criam requisições ao Medium.

O link textual do artigo EN para a versão portuguesa no Medium retornou HTTP 403 à consulta automatizada; não foi considerado quebrado nem validado como acessível. Foi preservado. Os quatro `originalUrl` permanecem metadados; disponibilidade de todos os artigos de proveniência não foi validada. Navegação local entre traduções foi validada separadamente.

## Validação

Hugo Extended **0.167.0**, Blowfish fixado no projeto. Comandos executados (binário disponível em `/tmp/portfolio-hugo/hugo`):

```bash
/tmp/portfolio-hugo/hugo version
/tmp/portfolio-hugo/hugo --minify --environment production --destination /tmp/medium-batch-production --noBuildLock --panicOnWarning
/tmp/portfolio-hugo/hugo --minify --buildDrafts --environment production --destination /tmp/medium-batch-preview --noBuildLock --panicOnWarning
git diff --check
```

- Builds com e sem drafts concluídos sem avisos: produção 6 páginas EN / 4 PT-BR; prévia 18 EN / 16 PT-BR (contagens Hugo incluem saídas auxiliares).
- Quatro URLs geradas somente com drafts. Títulos H1, descrições, canonical próprio, links internos, âncoras, `hreflang` e links entre traduções conferidos no HTML.
- Todos os 39 blocos de código renderizados conferidos contra o Markdown, sem perda do conteúdo.
- Firefox headless: quatro artigos em 375px e 1440px, CSS carregado, imagens carregadas após aguardar lazy loading e ausência de overflow da página. Capturas de prévia inspecionadas. Isso não substitui auditoria completa de acessibilidade ou Lighthouse, que não foram executados.
- Verificação dos arquivos novos com `git diff --no-index --check`: espaços finais dos originais foram preservados (incluem hard breaks Markdown e espaços em exemplos); conferência adicional com `core.whitespace=-blank-at-eol` não apontou outros problemas.
- Exemplos de infraestrutura não executados; nenhum resultado de segurança ou compatibilidade operacional é presumido pelo build.
- Listagens continuam ocultando drafts mesmo na prévia; acesso por URL direta é o comportamento preservado.

## Prévia local

Servidor iniciado em `http://localhost:1315/`, pois 1313 já estava ocupada:

- http://localhost:1315/articles/prompt-engineering-for-developers/
- http://localhost:1315/pt-br/articles/prompt-engineering-para-devs/
- http://localhost:1315/articles/composite-actions-reusable-workflows/
- http://localhost:1315/pt-br/articles/composite-actions-workflows-reutilizaveis/

Para reiniciar após encerrar esta sessão:

```bash
/tmp/portfolio-hugo/hugo server --buildDrafts --disableFastRender --bind 127.0.0.1 --port 1315 --baseURL http://localhost:1315/ --noBuildLock --renderToMemory
```

Qualquer commit, push, PR ou publicação depende de autorização específica. O lote permanece pendente de revisão humana.
