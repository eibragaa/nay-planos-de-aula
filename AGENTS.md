# Instruções para o Hermes

Este repositório é a fonte oficial dos planos semanais do Pré-Maternal da
Creche e Pré-Escola Planeta Bebê.

## Regra principal

Ao receber um pedido para criar, continuar, corrigir ou replicar planos de
aula, usar obrigatoriamente a skill `$gerar-planos-pre-maternal`. Ler por
inteiro `skill/gerar-planos-pre-maternal/SKILL.md` e seguir as referências que
ela indicar. O modelo DOCX incluído na skill é a autoridade visual e
estrutural; nunca reconstruir o documento do zero.

## Ambiente canônico no homelab

- Repositório: `/root/repositorio/nay-planos-de-aula`
- Python: `/root/repositorio/nay-planos-de-aula/.venv/bin/python`
- Skill: `/root/.hermes/skills/gerar-planos-pre-maternal`
- Saídas temporárias: `/root/repositorio/nay-planos-de-aula/outputs`

Para atualizar o ambiente:

```bash
cd /root/repositorio/nay-planos-de-aula
git pull --ff-only
./install.sh --hermes
hermes skills list
```

## Execução

1. Associar cinco temas, na ordem recebida, de segunda a sexta. Se houver um
   tema central, desdobrá-lo em cinco propostas coerentes.
2. Usar `America/Manaus` para calcular a próxima semana quando faltarem datas.
3. Selecionar somente objetivos EI02 presentes na referência BNCC da skill.
4. Preparar o JSON conforme `references/input-schema.md`.
5. Gerar o DOCX com `scripts/build_plan.py` e o Python da `.venv`.
6. Validar o ZIP, as cinco tabelas, as linhas 9/9/8/9/9, as datas, os temas e a
   ausência de conteúdo da semana anterior.
7. Entregar o DOCX final. Entregar o JSON somente quando solicitado.

Não alterar margens, tabelas, imagens, estilos, assinaturas ou quebras de
página. Não acessar nem revelar `.env`, `auth.json`, tokens ou chaves SSH para
gerar planos. Não publicar, enviar ou versionar uma saída sem pedido explícito.
