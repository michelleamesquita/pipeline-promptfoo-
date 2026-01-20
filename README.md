# Pipeline Promptfoo

Pipeline para gerar testes Red Team, avaliar com plugin e LLM‑as‑judge, calcular métricas e produzir um resumo por modelo.

## Pré‑requisitos

- `promptfoo` instalado
- `python3` instalado
- `OPENAI_API_KEY` configurada no ambiente

```bash
export OPENAI_API_KEY="sk-..."
```

## Estrutura principal

- `prompt.md`: prompt base do sistema
- `teste.yml`: config de red team + judge (gpt‑5) + providers
- `redteam-tests.yml`: testes gerados pelo red team
- `add_prompt_metrics.py`: gera `prompt_metrics.json`
- `summarize_scores.py`: gera `score_summary.md` com Risk Score e severidade


Saídas:
- `redteam-results.json` → avaliação do plugin (vulnerabilidade)
- `llm-judge-results.json` → avaliação do judge (LLM‑as‑judge)
- `prompt_metrics.json` → métricas de prompt
- `score_summary.md` → resumo com Risk Score, severidade e métricas

## Pipeline manual (passo a passo)

```bash
cd /Users/mac/Documents/pipeline-promptfoo
promptfoo redteam generate --force --config ./teste.yml --output ./redteam-tests.yml
promptfoo redteam eval -c ./redteam-tests.yml --output ./redteam-results.json
promptfoo eval -c ./redteam-tests.yml --output ./llm-judge-results.json
python3 add_prompt_metrics.py
python3 summarize_scores.py
```

## GitHub Actions

Workflow: `.github/workflows/promptfoo-pipeline.yml`

Requisitos:
- Secret `OPENAI_API_KEY`
- Environment `human-approval` com revisão manual

Artifacts por etapa:
- `redteam-tests`
- `llm-judge-results`
- `prompt-metrics`
- `score-summary`

## Risk Score

O Risk Score segue o modelo CVSS‑like descrito no projeto e adiciona os fatores:

- `prompt_density`
- `prompt_token_density`
- `prompt_line` (normalizado)

O resumo final inclui emoji de severidade:

- 🔴 critical
- 🟠 high
- 🟡 medium
- 🟢 low
- ⚪ none
