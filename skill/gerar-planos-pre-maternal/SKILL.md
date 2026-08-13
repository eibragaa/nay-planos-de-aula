---
name: gerar-planos-pre-maternal
description: Cria planos de aula semanais em DOCX para a turma Pré-Maternal da Creche e Pré-Escola Planeta Bebê, preservando fielmente o modelo institucional, os cinco dias, as tabelas, o logotipo, as assinaturas e a formatação. Use quando o usuário enviar um tema central, temas por dia, datas de uma semana ou pedir para replicar/continuar os planos existentes com campos de experiências, direitos e objetivos EI02 da BNCC, rotina, vivência e avaliação.
---

# Gerar planos do Pré-Maternal

Produzir uma cópia preenchida do modelo em `assets/modelo-planejamento-semanal.docx`. Nunca reconstruir o documento do zero.

## Fluxo obrigatório

1. Interpretar os temas informados.
   - Se houver cinco temas, associá-los de segunda a sexta na ordem recebida.
   - Se houver apenas um tema central, desdobrá-lo em cinco vivências coerentes e variadas.
   - Se as datas não forem informadas, usar a próxima semana de segunda a sexta no fuso local.
2. Preservar, salvo pedido explícito em contrário:
   - escola: `CRECHE E PRÉ-ESCOLA PLANETA BEBÊ`;
   - turma: `PRÉ-MATERNAL`;
   - professoras: `NAYARA VALETA / ANA.`;
   - professora titular e coordenadora já presentes nas assinaturas do modelo.
3. Ler `references/bncc-ei02.md` antes de selecionar objetivos. Usar apenas códigos EI02 e textos ali registrados. Marcar somente os campos de experiências correspondentes aos objetivos escolhidos.
4. Redigir cada dia no estilo dos planos existentes:
   - acolhida e `RODA DE CONVERSA`;
   - `ATIVIDADE DIRIGIDA` adequada a crianças bem pequenas;
   - materiais e espaços integrados à descrição quando necessário;
   - avaliação observacional com cinco critérios curtos;
   - linguagem pedagógica, acolhedora, prática e no futuro do presente.
5. Respeitar a capacidade fixa do modelo:
   - objetivos: 3/4/3/4/3, de segunda a sexta;
   - rotina: 4/3/2/2/2 parágrafos;
   - avaliação: 1 introdução + 5 critérios por dia.
6. Ler `references/input-schema.md`, criar um JSON temporário e executar:

   ```bash
   python scripts/build_plan.py --input /caminho/semana.json --output /caminho/plano.docx
   ```

7. Verificar o DOCX gerado:
   - abrir como ZIP sem erro;
   - confirmar 5 tabelas com 9/9/8/9/9 linhas;
   - confirmar datas, temas e ausência de conteúdo da semana anterior;
   - quando LibreOffice estiver disponível, renderizar as cinco páginas e inspecioná-las.
8. Entregar apenas o DOCX final, a menos que o usuário peça também o JSON.

## Regras de fidelidade

- Não alterar margens, imagens, bordas, larguras, estilos, assinaturas ou quebras de página.
- Não usar `python-docx` para salvar o modelo. O script modifica somente textos em `word/document.xml`.
- Não inventar códigos BNCC nem trocar a faixa EI02 por EI01/EI03.
- Não incluir atividades incompatíveis com crianças de 1 ano e 7 meses a 3 anos e 11 meses.
- Em temas folclóricos, adaptar a narrativa sem elementos assustadores ou conteúdo adulto.
- Manter a quarta-feira com 8 linhas; nela a avaliação não possui uma linha de título separada.
- Manter os textos próximos da densidade do modelo. Se a proposta ficar longa, resumir antes de gerar o DOCX.

## Uso no Linux

O gerador requer Python 3.10+ e `lxml`. Não requer Microsoft Word. O LibreOffice é opcional e serve somente para a conferência visual.

## Execução no Hermes

Quando a skill estiver vinculada em `/root/.hermes/skills`, localizar os
caminhos canônicos sem copiar a skill para outro lugar:

```bash
skill_dir="$(readlink -f /root/.hermes/skills/gerar-planos-pre-maternal)"
repo_dir="$(dirname "$(dirname "$skill_dir")")"
python_bin="$repo_dir/.venv/bin/python"
```

- Ler este arquivo inteiro e as duas referências indicadas no fluxo antes de
  criar o JSON.
- Usar `America/Manaus` para interpretar “próxima semana” quando o usuário não
  informar datas.
- Gravar arquivos finais em `$repo_dir/outputs`, salvo quando o usuário pedir
  explicitamente para versioná-los no repositório.
- Não ler, copiar ou expor `.env`, `auth.json`, tokens ou chaves SSH. O gerador
  não precisa de credenciais.
- Após atualizar o repositório, executar `./install.sh --hermes` e
  `hermes skills audit`.
