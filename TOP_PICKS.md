# Top Picks

Curated shortlist of high-value repositories to inspect first.

| # | Repository | Role | Why useful | Combine with |
|---:|---|---|---|---|
| 1 | [Agent-Field/agentfield](https://github.com/Agent-Field/agentfield) | Socle d'exécution agentique | Control plane orienté production : APIs, queues, retries, mémoire et observabilité. | AgentScope + CubeSandbox + OpenObserve |
| 2 | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | Framework multi-agents | Très bon candidat pour expérimenter orchestration, outils, MCP et observabilité des agents. | AgentField + Claude-mem |
| 3 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | Harness + montée en compétence | Concentre skills, mémoire, hooks, règles, sécurité et boucle d'amélioration des coding agents. | spec-kit + PR-Agent + Claude-mem |
| 4 | [cloudflare/cloudflare-os](https://github.com/cloudflare/cloudflare-os) | Workspace agentique complet | Référence architecturale forte pour contexte, agents, mini-apps sandboxées et intégrations sécurisées. | CubeSandbox + Supabase |
| 5 | [huangruiteng/loopx](https://github.com/huangruiteng/loopx) | Agents longue durée | Très pertinent pour workflows persistants, gouvernés et exécutés sur plusieurs harnesses. | Multica + Herdr |
| 6 | [Forward-Future/loopy](https://github.com/Forward-Future/loopy) | Patterns de boucles agentiques | Excellent catalogue de loops réutilisables pour formaliser les comportements d'agents. | ECC + agency-agents |
| 7 | [multica-ai/multica](https://github.com/multica-ai/multica) | Orchestration de coding agents | Permet de traiter les agents de code comme des coéquipiers assignables sur des issues. | Herdr + spec-kit + PR-Agent |
| 8 | [herdrdev/herdr](https://github.com/herdrdev/herdr) | Runtime pour coding agents | Intéressant comme couche d'exécution/workspace pour faire tourner plusieurs agents de développement. | Multica + LoopX |
| 9 | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | Agent évolutif | À étudier pour mémoire, personnalisation et évolution de comportement dans le temps. | Claude-mem + Loopy |
| 10 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | Mémoire persistante | Brique directement alignée avec l'objectif de capitaliser contexte et apprentissages entre sessions. | ECC + Khoj |
| 11 | [obra/superpowers](https://github.com/obra/superpowers) | Skills de développement | Bon matériau pour une bibliothèque commune de skills et workflows de qualité. | ECC + spec-kit |
| 12 | [github/spec-kit](https://github.com/github/spec-kit) | Specification-driven development | Structure très bien la phase specs → plan → implémentation pour une stack Feature Development. | Multica + PR-Agent |
| 13 | [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) | Reviewer automatique | Candidat naturel pour le rôle Reviewer/Critic dans une stack de développement. | spec-kit + Repowise |
| 14 | [repowise-dev/repowise](https://github.com/repowise-dev/repowise) | Compréhension de codebase | Utile comme couche de contexte pour agents travaillant sur de grands dépôts. | PR-Agent + Claude-mem |
| 15 | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | Bibliothèque de rôles | Très bonne source pour constituer une librairie d'agents réutilisables par métier. | 500-AI-Agents + Loopy |
| 16 | [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) | Catalogue d'agents | Large base d'idées, exemples et cas d'usage à indexer comme knowledge base. | agency-agents + awesome-llm-apps |
| 17 | [TencentCloud/CubeSandbox](https://github.com/TencentCloud/CubeSandbox) | Sandbox agents/code | Brique importante pour isoler l'exécution d'outils et de code produit par les agents. | AgentField + Strix |
| 18 | [czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp) | MCP ↔ n8n | Permet de faire de n8n une couche d'actions/workflows pilotable par des agents. | n8n-workflows + Postiz |
| 19 | [Zie619/n8n-workflows](https://github.com/Zie619/n8n-workflows) | Bibliothèque de workflows | Source de workflows réutilisables à transformer en capacités métier de stacks. | n8n-mcp + awesome-n8n-templates |
| 20 | [gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | Distribution de contenu | Très pertinent pour une stack Growth/Content avec publication multi-réseaux. | n8n + MoneyPrinterTurbo + Plausible |
| 21 | [nowork-studio/notfair-plugin](https://github.com/nowork-studio/notfair-plugin) | SEO/GEO/Marketing skills | Pack spécialisé immédiatement réutilisable pour une stack Growth Marketing. | Postiz + Plausible |
| 22 | [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | Génération vidéo automatisée | Base solide pour une content factory automatisée. | Whisper + OpenCut + Postiz + n8n |
| 23 | [HKUDS/VideoRAG](https://github.com/HKUDS/VideoRAG) | RAG vidéo | Permet d'indexer et exploiter des contenus vidéo dans une base de connaissances. | MinerU + Whisper + Khoj |
| 24 | [khoj-ai/khoj](https://github.com/khoj-ai/khoj) | Assistant knowledge personnel | Très intéressant pour mémoire longue durée, recherche personnelle et RAG self-hosted. | AppFlowy + MinerU + screenpipe |
| 25 | [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | Ingestion documentaire | Bonne brique d'extraction/structuration avant indexation RAG. | Khoj + PixelRAG |
| 26 | [openai/whisper](https://github.com/openai/whisper) | Transcription | Composant fiable pour transformer audio/vidéo en données exploitables par des agents. | VideoRAG + KrillinAI |
| 27 | [Osmantic/ODS](https://github.com/Osmantic/ODS) | Serveur IA local complet | Option intéressante pour disposer rapidement d'un environnement local LLM/RAG/agents/voix. | Open WebUI + n8n |
| 28 | [usestrix/strix](https://github.com/usestrix/strix) | AppSec agentique | Très pertinent pour une stack DevSecOps avec audit automatisé sur périmètre autorisé. | KICS + Semgrep + Plumber |
| 29 | [getplumber/plumber](https://github.com/getplumber/plumber) | Sécurité CI/CD | Complète bien une stack DevSecOps focalisée GitHub Actions/pipelines. | KICS + Semgrep |
| 30 | [Checkmarx/kics](https://github.com/Checkmarx/kics) | IaC security | Brique directe de contrôle Terraform/Kubernetes/CloudFormation dans les pipelines. | Plumber + Infracost |
| 31 | [infracost/actions](https://github.com/infracost/actions) | FinOps CI | Permet d'ajouter le coût comme signal dès la pull request IaC. | Terraform Skill + KICS |
| 32 | [robusta-dev/krr](https://github.com/robusta-dev/krr) | Rightsizing Kubernetes | Très utile pour FinOps/Capacity Planning à partir de l'usage réel. | OpenObserve + Infracost |
| 33 | [openobserve/openobserve](https://github.com/openobserve/openobserve) | Observabilité | Bon candidat self-hosted pour centraliser logs/métriques/traces des stacks et agents. | AgentField + KRR |
| 34 | [solo-io/gitops-library](https://github.com/solo-io/gitops-library) | Patterns GitOps | Référence utile pour industrialiser les stacks sur Kubernetes. | Terraform + KICS + OpenObserve |
| 35 | [supabase/supabase](https://github.com/supabase/supabase) | Backend rapide | Excellent backend pour prototyper auth, DB, storage, APIs et realtime autour d'applications personnelles. | Twenty + Postiz + agents |
| 36 | [AppFlowy-IO/AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) | Knowledge workspace | Peut servir d'interface ou de source de connaissances pour des projets personnels/agents. | Khoj + MinerU |
