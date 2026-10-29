# PROJECT_BRIEF.md — Portfólio Profissional e Blog Técnico

> **Status:** Foundation implementada localmente / v1.2 — 29/10/2026; revisão humana pendente\
> **Responsável pelo produto:** proprietário do portfólio  
> **Execução:** Codex, com revisões humanas  
> **Documento complementar:** [`AGENTS.md`](./AGENTS.md)

## 1. Visão do produto

Construir um **portfólio profissional e blog técnico pessoal**, público, estático, bilíngue (inglês e português brasileiro), com imagem de liderança sênior em tecnologia e conteúdo técnico de qualidade.

O site deve apoiar dois objetivos, nesta ordem:

1. **Empregabilidade:** aumentar a credibilidade do perfil perante recrutadores e hiring managers de posições remotas, nacionais ou internacionais, com foco principal em liderança de Platform Engineering, DevOps e SRE. Cloud Architecture e GenAI são temas secundários, sujeitos à validação do conteúdo.
2. **Autoridade profissional e consultoria:** demonstrar repertório técnico e capacidade de conectar decisões de engenharia a resultados de negócio, abrindo caminho para oportunidades B2B.

O portfólio deve complementar — não reproduzir literalmente — o LinkedIn e o currículo. **Não é uma loja, SaaS, sistema de cadastro nem um currículo visual genérico.**

### 1.1 Posicionamento editorial proposto

**Headline em inglês — rascunho para revisão:**

> Platform Engineering, DevOps & SRE Leader

O foco profissional foi confirmado na Fase 0. A redação final da headline e das mensagens abaixo permanece sujeita à revisão editorial antes da publicação.

**Mensagem central — rascunho para revisão:**

> I help teams build reliable, secure and scalable engineering platforms, combining hands-on architecture with technology leadership and a pragmatic approach to automation and AI.

**Versão portuguesa — rascunho para revisão:**

> Ajudo equipes a construir plataformas de engenharia confiáveis, seguras e escaláveis, combinando arquitetura prática, liderança tecnológica e uma abordagem pragmática de automação e IA.

Não utilizar números, títulos, certificações ou resultados não confirmados. A trajetória profissional de mais de três décadas em TI e a experiência em liderança, DevOps, GenAI, gestão de ambientes e atividades de TPM podem orientar o conteúdo, **sujeitas à validação do proprietário** antes de publicar.

## 2. Públicos-alvo e jornadas

| Público | O que precisa entender em 30–60 segundos | Ação desejada |
| --- | --- | --- |
| Recrutador técnico | Senioridade, especialidades, atuação e idiomas | Abrir LinkedIn ou iniciar contato |
| Hiring manager / CTO / VP Engineering | Contexto de liderança, qualidade das decisões e experiência arquitetural | Ler Sobre e um artigo/case |
| Potencial cliente de consultoria | Problemas que o profissional sabe resolver, metodologia e segurança | Solicitar uma conversa |
| Comunidade técnica | Exemplos concretos e conteúdo útil | Ler, citar ou compartilhar artigos |

### Critérios de sucesso (sem prometer tráfego ou contratações)

- Em **até três cliques**, chegar de qualquer página a Sobre, Artigos e Contato.
- Em **até 30 segundos**, a primeira dobra da home comunica área de atuação, senioridade e caminho de contato.
- Conteúdo importante disponível em inglês e português, com navegação entre idiomas.
- Páginas públicas indexáveis, com SEO técnico correto.
- Publicação de um novo artigo predominantemente via arquivo Markdown + revisão + pipeline.
- Resultados de recrutamento e contatos poderão ser acompanhados manualmente; métricas de tráfego só serão adicionadas se houver decisão explícita sobre privacidade.

## 3. Escopo funcional

### 3.1 MVP obrigatório

1. **Home:** apresentação objetiva, chamada principal, áreas de especialidade, destaques de artigos e CTAs para LinkedIn/contato.
2. **About / Sobre:** trajetória profissional, evolução de responsabilidades, visão de engenharia e liderança, com fatos aprovados.
3. **Articles / Artigos:** listagem, filtros/tags adequados ao tema, página individual, data, tempo de leitura, navegação e compartilhamento por link.
4. **Projects & Case Studies / Projetos e Cases:** estudos de caso públicos ou anonimizados, diferenciando claramente projeto pessoal, proposta arquitetural e experiência profissional.
5. **Contact / Contato:** LinkedIn, GitHub público e e-mail profissional **somente após autorização**. Preferir links externos ou `mailto:`; não criar backend nem coletar dados.
6. **Idiomas:** inglês como idioma padrão em `/`; português brasileiro em `/pt-br/`; seletor de idioma visível.
7. **Tema:** opção de modo claro/escuro conforme capacidades do Blowfish, com boa legibilidade em ambos.
8. **SEO:** título e descrição por página, canonical, Open Graph, sitemap, robots, links internos, marcação semântica e `hreflang` quando as traduções existirem.
9. **Deploy:** GitHub Pages por GitHub Actions, com checagem de build para mudanças propostas e deploy apenas a partir da branch de publicação autorizada.
10. **Manutenção:** README com instruções de edição/publicação e modelos para novos artigos/cases.

### 3.2 Fora do MVP

- CMS, WordPress, banco de dados, login, área administrativa, comentários hospedados, newsletter com coleta de e-mails ou formulários com backend.
- App JavaScript complexo, microserviços, containers de produção, Kubernetes ou infraestrutura própria para hospedar o site.
- Autopublicação de textos gerados por IA sem revisão humana.
- Integração com repositórios privados do Gitea ou exposição de código proprietário.
- Dashboard de analytics com cookies, pixels de anúncios ou trackers de terceiros por padrão.
- Tradução automática em tempo de execução.

## 4. Estrutura de navegação e conteúdo

### Navegação principal

| EN (padrão) | PT-BR | Objetivo |
| --- | --- | --- |
| Home | Início | Posicionamento e direcionamento |
| About | Sobre | Carreira e diferenciais |
| Articles | Artigos | Conhecimento e autoridade |
| Projects | Projetos | Evidências de capacidade técnica |
| Contact | Contato | Conversão |

### 4.1 Home — composição sugerida

1. **Hero:** Ivan Claudio Fernandes (nome curto: IvanCl4udio), headline, descrição de duas a três linhas e CTAs: `View my work` / `Connect on LinkedIn`, com textos e links aprovados antes de publicar.
2. **Expertise:** Platform Engineering & DevOps; SRE & Observability; Cloud & Software Architecture; Generative AI & Automation; Engineering Leadership.
3. **Selected work:** até dois ou três cards, conforme disponibilidade de projetos/cases **autorizados**; omitir enquanto não houver conteúdo aprovado.
4. **Latest insights:** até três artigos publicados; omitir enquanto não houver conteúdo aprovado.
5. **Professional journey:** resumo da trajetória e link para Sobre.
6. **Footer:** links profissionais, idiomas, copyright e política simples de privacidade, se necessária.

### 4.2 Sobre

Cobrir: introdução executiva, especialidades, experiência em liderança, visão de arquitetura e operações, evolução profissional e foco atual. Organizar para leitura rápida com seções curtas e parágrafos de substância. Evitar exposição de idade, informações familiares, remuneração, planos privados, motivos da procura de emprego e nomes de equipes ou sistemas internos.

**Identidade confirmada na Fase 0:**

- Nome profissional: **Ivan Claudio Fernandes**.
- Nome curto: **IvanCl4udio**.
- Conta GitHub: **IvanCl4udio**.
- Foco principal: **liderança de Platform Engineering, DevOps e SRE**.

**Dados pendentes de confirmação antes de publicar:**

- `[URL_LINKEDIN]` (candidato informado anteriormente: `https://www.linkedin.com/in/ivanclaudio/`, validar antes de publicar).
- `[EMAIL_PUBLICO]` e consentimento para exibi-lo.
- `[BIO_APROVADA_EN]` e `[BIO_APROVADA_PT_BR]`.
- `[EMPRESAS_E_CARGOS_PUBLICAVEIS]`, `[PERIODOS]`, `[FORMACAO]`, `[CERTIFICACOES]`.
- `[CASES_PUBLICAVEIS]`, `[RESULTADOS_COM_EVIDENCIAS]` e `[FOTO_APROVADA]` (foto opcional).
- `[DOMINIO_CUSTOMIZADO]` (opcional e somente após o MVP).

### 4.3 Projetos e cases — modelo editorial

Cada case deve ter: contexto e desafio; papel do profissional; restrições; trade-offs; solução e arquitetura; segurança/observabilidade quando relevante; resultados **somente se comprovados e autorizados**; aprendizados; referências públicas. Se o trabalho for conceitual, identificar como **reference architecture** ou **personal lab project**, nunca como implantação comprovada em cliente.

É possível publicar conteúdos sobre laboratório pessoal e Kubernetes de modo agregado. Não revelar DNS internos, IPs privados, endpoints, topologia detalhada de segurança, segredos, credenciais ou quaisquer dados que possam facilitar ataques à infraestrutura pessoal ou corporativa.

## 5. Linha editorial — artigos iniciais sugeridos

| Prioridade | Título de trabalho (EN) | Entrega de valor | Natureza |
| --- | --- | --- | --- |
| P1 | **Designing a Practical DevOps Maturity Score** | Critérios verificáveis para CI/CD, testes, SAST/DAST e deploy | Framework conceitual; sem revelar IP de produto |
| P1 | **Modern Kubernetes Observability with Prometheus, Loki, Grafana and Alloy** | Decisões de arquitetura e trade-offs operacionais | Exemplo reproduzível de laboratório seguro |
| P2 | **AI Agents for Platform Engineering: Where Automation Helps—and Where Humans Decide** | Aplicações pragmáticas, controles, segurança e governança | Artigo opinativo técnico fundamentado |
| P2 | **Engineering Leadership: Balancing Reliability, Delivery and Business Outcomes** | Gestão, priorização, indicadores e tomada de decisão | Reflexões de liderança sem dados internos |

**Regra editorial:** artigos com exemplos testados, referências para afirmações externas e explicação de limitações. Publicar somente versões revisadas; artigos/cases podem ter tradução adicionada posteriormente, sem gerar página fictícia ou `hreflang` para tradução ausente. Não usar tradução literal de baixa qualidade. Não publicar resumos de material confidencial ou derivados de repositórios privados. As pautas acima são sugestões, não evidências de experiência ou de projetos realizados.

## 6. Direção visual e UX

- **Estética:** sóbria, executiva, tecnológica, minimalista e moderna; mais próxima de um site pessoal de engineering leader do que de um dashboard ou currículo repleto de badges.
- **Tema base:** Blowfish v3, customizações moderadas. Usar recursos nativos antes de desenvolver componentes próprios.
- **Tipografia:** legível em desktop e mobile, ótima hierarquia visual, largura de leitura confortável para artigos técnicos.
- **Cores:** paleta neutra com um único acento visual; contraste adequado em dark/light mode. Paleta específica será escolhida em revisão visual.
- **Imagens:** evitar imagens genéricas de IA, falsas fotos corporativas ou marcas de empresas sem permissão. Preferir diagramas próprios e foto aprovada, se houver.
- **Mobile first:** menu, grids, cards, hero, imagens e blocos de código sem overflow horizontal.
- **Acessibilidade:** WCAG 2.2 AA como objetivo; navegação por teclado, foco visível, headings semânticos, `alt` descritivo, contraste, respeitar `prefers-reduced-motion`.
- **Performance:** HTML estático, CSS/JS enxutos, imagens otimizadas; sem efeitos que prejudiquem Core Web Vitals.

## 7. Internacionalização e SEO

- Configurar os idiomas `en` e `pt-br` de acordo com as convenções documentadas do Hugo/Blowfish (`languages.en.toml` e `languages.pt-br.toml`, ou configuração equivalente suportada pela versão escolhida).
- Inglês por padrão na raiz; português brasileiro em `/pt-br/`. Se a versão instalada exigir alteração de caminhos, documentar a decisão antes de implementar.
- Configurar `defaultContentLanguage = "en"` e preferir URL estável sem redirecionamento inesperado na raiz.
- Manter **slugs consistentes dentro de cada idioma** e URLs permanentes depois da publicação. Usar tradução equivalente apenas quando o conteúdo realmente existir.
- Gerar metadata `title`, `description`, canonical e metadados sociais por conteúdo; favicon/og-image próprios quando aprovados.
- Produzir sitemap e robots.txt válidos; impedir indexação de ambientes de prévia, se forem criados.
- Validar alternância de idiomas e `hreflang` sem criar referências para traduções inexistentes.
- Páginas institucionais devem ter conteúdo equivalente em EN/PT-BR antes do lançamento. Artigos e cases podem existir inicialmente em um único idioma, com vínculo entre traduções apenas quando ambas existirem e estiverem revisadas.
- Não prometer posicionamento no Google ou visibilidade garantida em recrutadores.

## 8. Arquitetura técnica

| Camada | Escolha | Justificativa |
| --- | --- | --- |
| Gerador | **Hugo Extended** (versão estável compatível e fixada) | Build estático rápido e suporte a Markdown |
| Tema | **Blowfish v3** | Recursos prontos para blog, perfil e i18n |
| Gerência do tema | **Hugo Module** preferencial, com `go.mod`/`go.sum` versionados | Reprodutibilidade; não copiar código do tema |
| Hospedagem | **GitHub Pages** | Baixa manutenção, HTTPS e URL pública |
| CI/CD | **GitHub Actions** | Testes, build e deploy controlado |
| Conteúdo | **Markdown + front matter** | Edição simples, histórico Git, sem CMS |
| Versionamento público | **GitHub apenas para o site** | Separação dos projetos proprietários no Gitea |

Usar a versão de Hugo **0.162.0 ou superior**, respeitando o mínimo atualmente documentado pelo Blowfish; registrar no README a versão exata validada e fixar a mesma no CI. Verificar compatibilidade e documentação no momento da implementação. No uso de Hugo Modules, seguir o módulo do Blowfish v3 (`github.com/nunocoracao/blowfish/v3`), sem adicionar `theme = "blowfish"` como se fosse uma instalação por submódulo Git.

Versões validadas na Foundation: **Hugo Extended 0.167.0**, **Blowfish v3.9.0** e **Go 1.25.6**. O tema declara faixa Hugo Extended 0.164.0–0.167.0; Hugo 0.169.0 foi descartado após aviso de incompatibilidade.

### Estrutura alvo (ajustar às convenções efetivas do tema)

```text
.
├── AGENTS.md
├── PROJECT_BRIEF.md
├── README.md
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── config/
│   └── _default/
│       ├── hugo.toml
│       ├── module.toml
│       ├── languages.en.toml
│       ├── languages.pt-br.toml
│       ├── menus.en.toml
│       ├── menus.pt-br.toml
│       ├── params.toml
│       └── markup.toml
├── content/
│   ├── en/
│   │   ├── _index.md
│   │   ├── about.md
│   │   ├── articles/
│   │   ├── projects/
│   │   └── contact.md
│   └── pt-br/
│       ├── _index.md
│       ├── about.md
│       ├── articles/
│       ├── projects/
│       └── contact.md
├── assets/
├── static/
├── archetypes/
├── go.mod
└── go.sum
```

A árvore é **alvo lógico**, não imposição para fabricar arquivos vazios ou desrespeitar layouts do Blowfish. Arquivos opcionais serão criados conforme o projeto evoluir.

### 8.1 Repositório e domínio

- Conta e repositório confirmados pelo proprietário: **`IvanCl4udio/IvanCl4udio.github.io`**, destinado exclusivamente ao site público. Não criar outro repositório.
- URL pretendida e confirmada: **`https://ivancl4udio.github.io/`**. Essa decisão não comprova visibilidade remota, ativação do Pages ou publicação.
- Branch de integração/publicação: `main`, com merge/revisão controlados; trabalho em branches `feat/*`, `content/*` ou `fix/*`.
- Na inspeção local da Fase 0, a branch atual era `master`. Tratar explicitamente a transição para `main` antes de qualquer mudança; não alterar configurações remotas sem autorização específica.
- Um domínio próprio é fase opcional. Não mudar DNS nem adicionar `CNAME` sem autorização.
- Código proprietário, dados de clientes e materiais internos **permanecem fora** do GitHub público.

### 8.2 CI/CD e segurança

1. **Pull requests / branches:** validar configuração, integridade de links locais quando viável, testes de conteúdo e build Hugo em modo de produção; **não fazer deploy**.
2. **`main`:** executar build e publicar somente se a configuração de produção tiver sido aprovada pelo proprietário; merge em `main` após ativação do deploy significa publicação automática — deixar isso explícito em toda revisão.
3. **GitHub Pages:** usar `actions/configure-pages`, `actions/upload-pages-artifact` e `actions/deploy-pages` em versões atuais, além do checkout, com permissões mínimas adequadas a cada job (`contents: read`, `pages: write`, `id-token: write` onde necessário).
4. **Segurança:** sem tokens pessoais, SSH keys ou secrets no código. Evitar dependências e GitHub Actions não verificadas; preferir versões pinadas e atualizar deliberadamente.
5. **Build reproduzível:** mesma versão do Hugo em local/CI, dependências fixadas, pasta de saída `public/` ignorada pelo Git e artefato efêmero para Pages.

## 9. Fases de execução e gates

| Fase | Entrega | Gate de aprovação |
| --- | --- | --- |
| **0 — Discovery** | Confirmar identidade, foco, URL, idiomas e conteúdo inicial; consolidar decisões nos documentos após autorização | Consolidação documental autorizada; implementação depende de aprovação separada |
| **1 — Foundation** | Hugo + Blowfish + README + configurações EN/PT + archetypes + estrutura e demonstrações em draft + CI básico sem deploy | Build local sem erros e validação da exclusão dos drafts; CI verificável quando sua execução remota for autorizada |
| **2 — Design & Content** | Home, Sobre, Articles, Projects, Contact e exemplos de conteúdo | Revisão visual desktop/mobile; textos aprovados |
| **3 — Quality & SEO** | Metadata, sitemap, accessibility, performance, links, i18n | Checklist de QA aprovado |
| **4 — Preparar publicação** | Revisar CI existente e preparar workflow de GitHub Pages, sem ativar Pages nem publicar | Workflows revisados; execução remota somente quando autorizada |
| **5 — Launch** | Ativar Pages, merge/deploy e smoke test público | Autorização explícita de publicação |
| **6 — Operação** | Pauta recorrente, atualização de artigos e backlinks no LinkedIn | Conteúdo revisado artigo a artigo |

O Codex deve **propor o plano e aguardar aprovação antes de fazer a primeira alteração**. Após essa autorização, pode implementar a fase aprovada, mas não deve criar novos repositórios, alterar configurações remotas, fazer push, merge, deploy ou mudanças de DNS sem nova autorização específica.

**Escopo confirmado para planejar a Foundation:** EN principal e PT-BR secundário; conteúdo demonstrativo apenas em draft, excluído do build público. Bio, contatos, foto e cases dependem de aprovação posterior. Não presumir trajetória, certificações, resultados ou experiências. A Foundation recebeu aprovação separada após a consolidação documental da Fase 0. Sua implementação local não autoriza ações remotas ou início das fases seguintes.

## 10. Definition of Done do MVP

- [ ] Site gerado com Hugo e Blowfish, sem backend.
- [ ] Build limpo e reproduzível em ambiente local e CI.
- [ ] Home, Sobre, Artigos, Projetos e Contato presentes nos dois idiomas, com conteúdo aprovado (sem textos fictícios públicos).
- [ ] Seletor EN/PT-BR funciona; navegação e URLs corretas.
- [ ] Layout revisado em mobile (375px), tablet (~768px) e desktop (~1440px), sem overflow.
- [ ] Navegação por teclado, foco, contraste, headings e textos alternativos revisados.
- [ ] Nenhum link interno quebrado; URLs externas críticas verificadas.
- [ ] Metadados SEO e sociais, canonical, sitemap e robots validados.
- [ ] Lighthouse **alvo ≥ 90** em Performance, Accessibility, Best Practices e SEO para páginas representativas, em ambiente e condições documentados; caso não atinja, registrar problemas e plano de correção, sem mascarar resultados.
- [ ] Nenhum segredo, dado corporativo restrito ou material proprietário no repositório/histórico.
- [ ] README ensina a rodar localmente, criar artigo, revisar e publicar.
- [ ] CI valida PR sem publicar; deploy somente após autorização e merge na branch de publicação.
- [ ] Site público acessível por HTTPS e links do LinkedIn revisados **após** o lançamento.

## 11. Decisões confirmadas e pendentes

Confirmados na Fase 0: identidade e foco descritos na seção 4.2, conta/repositório e URL da seção 8.1, inglês como idioma principal, PT-BR como secundário e conteúdo inicial demonstrativo somente em draft.

| Decisão | Padrão inicial | Quem aprova |
| --- | --- | --- |
| Domínio próprio | Não utilizar no MVP | Proprietário |
| Foto no hero | Não usar até receber foto aprovada | Proprietário |
| Nome de empregador atual e histórico | Não publicar sem validação | Proprietário |
| E-mail público | Não exibir até autorização | Proprietário |
| Disponibilidade profissional explícita | Não escrever “Open to Work” sem autorização | Proprietário |
| Contato para consultoria | Apenas link de contato sem promessa comercial | Proprietário |
| Analytics | Desabilitado no MVP | Proprietário |
| Exposição de projetos proprietários | Apenas referências genéricas autorizadas | Proprietário |

## 12. Referências técnicas a conferir durante a execução

- Hugo + GitHub Pages: <https://gohugo.io/host-and-deploy/deploy-to-github-pages/>
- Blowfish — instalação: <https://blowfish.page/docs/installation/>
- Blowfish — configuração: <https://blowfish.page/docs/configuration/>
- GitHub Pages — origem de publicação: <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>
- Codex — instruções do projeto (`AGENTS.md`): <https://learn.chatgpt.com/docs/agent-configuration/agents-md>

> **Nota:** este documento define intenção e requisitos; o agente deve checar as versões/documentações efetivamente vigentes e propor ajustes antes de instalar componentes. Nenhuma ação externa fica autorizada por este arquivo isoladamente.
