# Planos de Aula — Pré-Maternal

Repositório dos planejamentos semanais da turma Pré-Maternal da Creche e Pré-Escola Planeta Bebê. Inclui o modelo Word original e uma skill para gerar novos planos a partir de um tema central ou de cinco temas diários.

## Instalar no homelab com Hermes

```bash
mkdir -p /root/repositorio
cd /root/repositorio
git clone https://github.com/eibragaa/nay-planos-de-aula.git
cd nay-planos-de-aula
chmod +x install.sh
./install.sh --hermes
hermes skills list
```

O instalador cria `.venv`, instala `lxml` e vincula a skill em
`/root/.hermes/skills/gerar-planos-pre-maternal`. Abra uma nova sessão do
Hermes após a primeira instalação.

O arquivo `AGENTS.md` contém as regras que o Hermes deve seguir ao trabalhar
dentro deste repositório. O procedimento completo está em
`skill/gerar-planos-pre-maternal/SKILL.md`.

Para instalar no Codex, use `./install.sh --codex`. Para disponibilizar a skill
nos dois agentes, use `./install.sh --both`.

## Pedir ao Hermes ou ao Codex

Exemplo com temas diários:

```text
Use $gerar-planos-pre-maternal para criar a semana de 17 a 21/08/2026:
segunda, parque de areia; terça, lenda do Saci e pintura coletiva;
quarta, lenda da Iara; quinta, lenda do boto; sexta, dia do brinquedo.
```

Exemplo com apenas um tema:

```text
Use $gerar-planos-pre-maternal. Tema central: animais da floresta.
```

Se as datas não forem informadas, a skill usa a próxima semana de segunda a sexta.

## Atualizar no homelab

```bash
cd nay-planos-de-aula
git pull --ff-only
./install.sh --hermes
hermes skills list
```

## Gerar manualmente

Depois de preparar um JSON conforme `skill/gerar-planos-pre-maternal/references/input-schema.md`:

```bash
.venv/bin/python skill/gerar-planos-pre-maternal/scripts/build_plan.py \
  --input semana.json \
  --output outputs/plano-semanal.docx
```

O gerador modifica somente os textos do modelo. Word não é necessário; LibreOffice é opcional para conferir visualmente o resultado.
