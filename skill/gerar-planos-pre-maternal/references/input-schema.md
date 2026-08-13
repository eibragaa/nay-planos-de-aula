# Formato de entrada

Criar um JSON UTF-8 com cinco dias consecutivos, de segunda a sexta.

```json
{
  "metadata": {
    "class": "PRÉ-MATERNAL",
    "teachers": "NAYARA VALETA / ANA."
  },
  "days": [
    {
      "date": "2026-08-17",
      "fields": ["eu-outro-nos", "corpo-gestos-movimentos"],
      "rights": ["conviver", "brincar", "participar", "explorar", "expressar", "conhecer-se"],
      "objectives": [
        "EI02EO03 – Compartilhar os objetos e os espaços com crianças da mesma faixa etária e adultos.",
        "EI02CG02 – Deslocar seu corpo no espaço, orientando-se por noções como em frente, atrás, no alto, embaixo, dentro, fora etc., ao se envolver em brincadeiras e atividades de diferentes naturezas.",
        "EI02CG05 – Desenvolver progressivamente as habilidades manuais, adquirindo controle para desenhar, pintar, rasgar, folhear, entre outros."
      ],
      "routine": [
        "RODA DE CONVERSA – ...",
        "ATIVIDADE DIRIGIDA – ...",
        "Durante a atividade, ...",
        "A proposta favorecerá ..."
      ],
      "evaluation": [
        "A avaliação será realizada por meio da observação da professora, considerando:",
        "da participação durante a atividade;",
        "da exploração dos materiais;",
        "da coordenação motora;",
        "da interação com os colegas;",
        "do interesse e envolvimento na proposta."
      ]
    }
  ]
}
```

Repetir o objeto diário até completar cinco dias.

## Capacidades

| Dia | Objetivos | Rotina | Avaliação |
|---|---:|---:|---:|
| Segunda | 3 | 4 | 6 |
| Terça | 4 | 3 | 6 |
| Quarta | 3 | 2 | 6 |
| Quinta | 4 | 2 | 6 |
| Sexta | 3 | 2 | 6 |

## Chaves de campos

- `eu-outro-nos`
- `corpo-gestos-movimentos`
- `tracos-sons-cores-formas`
- `escuta-fala-pensamento-imaginacao`
- `espacos-tempos-quantidades`

## Chaves de direitos

- `conviver`
- `brincar`
- `participar`
- `explorar`
- `expressar`
- `conhecer-se`

Datas aceitas: `AAAA-MM-DD`, `DD/MM/AAAA` ou `DD/MM/AA`. O script calcula a linha `SEMANA:` e o dia da semana.
