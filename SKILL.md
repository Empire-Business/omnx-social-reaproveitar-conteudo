---
name: omnx-social-reaproveitar-conteudo
description: "Lê uma peça longa que já existe (live, podcast, aula, webinário, artigo), acha os trechos que se sustentam sozinhos, confere minutagem e citação por script e monta o plano de derivados por plataforma. Use quando pedirem 'reaproveita essa live', 'o que dá para tirar desse podcast', 'quais os melhores trechos dessa aula', 'transforma esse artigo em conteúdo', 'esse material vira o quê?', 'marca os cortes dessa transcrição', 'repurpose'. Entrega o plano, sem escrever os roteiros nem cortar o vídeo. Não use para criar conteúdo do zero, planejar o mês ou escrever roteiro de Reels (cami), cortar ou legendar o vídeo (cortez), copy de venda (rita), nem transcrever o vídeo (omnx-youtube-transcrever-video)."
---

# Reaproveitar conteúdo

Lê uma peça longa que já existe, encontra os trechos bons e entrega um plano: quais trechos viram quais conteúdos, em qual plataforma. Trabalha só com o que está na peça. Quem escreve o roteiro final ou corta o vídeo é outra etapa.

## Como conversar

Quem usa pode nunca ter feito isso. Se a pessoa chegar sem contexto, diga em duas linhas o que você faz e peça a transcrição ou o texto. Uma pergunta por vez. Palavra técnica vem com meia frase de explicação. Toda resposta termina com o próximo passo. A pessoa nunca precisa digitar comando.

## Passos

1. **Receba o texto da peça.** Aceita: transcrição em `.srt` ou `.vtt`, texto com minutagem (`12:03 frase`) ou texto corrido. Com só um link de vídeo ou áudio, explique que você precisa do texto e sugira transcrever antes. Pergunte quem é o autor da peça: se for de outra pessoa, avise que reaproveitar exige autorização dela.
2. **Pergunte só o que falta:** para quais plataformas é o conteúdo e qual o objetivo (alcance, leads, autoridade, venda). Se a pessoa tiver um tom de marca definido, leia.
3. **Leia a peça inteira.** Rode, a partir da pasta deste `SKILL.md`:

   ```
   python3 scripts/conferir_trechos.py listar <transcricao>
   ```

   O resultado é o texto com a minutagem de cada fala. Em texto corrido, cada parágrafo vira `[p1]`, `[p2]`.
4. **Escolha os trechos.** Procure:
   - Vídeo ou áudio: frase que resume uma ideia, história com começo, meio e fim, dado ou exemplo concreto, opinião contra o senso comum, demonstração de como se faz, momento de emoção real.
   - Texto: a tese central, cada argumento que se sustenta sozinho, histórias e exemplos, as frases mais fortes.

   Critério que decide: **quem nunca viu a peça entende o trecho sozinho?** Se precisar de dois minutos de contexto, ou ele sai, ou você indica o que acrescentar na abertura. Entra o que é bom: se só dois trechos prestam, são dois. Não complete uma quantidade.
5. **Confira no script.** Grave os escolhidos num JSON e rode:

   ```
   python3 scripts/conferir_trechos.py conferir <transcricao> <trechos.json>
   ```

   ```json
   [{"id": "T1", "inicio": "12:03", "fim": "12:48"}, {"id": "T2", "citacao": "frase exata do texto"}]
   ```

   Use `inicio` e `fim` quando houver minutagem e `citacao` em texto corrido. O `fim` é o instante em que o trecho acaba: a fala que começa exatamente nele fica de fora. A duração é o fim menos o início. O script devolve o texto exato, a duração e `ok`. Se vier `ok: false`, corrija o trecho ou tire-o do plano. Toda citação do plano vem dessa saída, palavra por palavra.
6. **Monte o plano.** Para cada trecho, escolha o derivado que combina com o conteúdo dele e consulte a adaptação por plataforma abaixo. Diga o porquê em poucas palavras e proponha uma frase de abertura. Limites de duração e de caracteres: confira na documentação atual da plataforma quando importar.
7. **Entregue no formato abaixo** e pergunte quais derivados a pessoa aprova. Salve em arquivo só se ela pedir, no lugar que indicar.

## Mapa por tipo de origem

| Origem | Derivados que costumam combinar |
|---|---|
| Live, podcast, entrevista | Corte de vídeo curto, trecho transcrito em post de texto, frase forte em card, resumo para e-mail ou lista de transmissão |
| Aula ou webinário | Série de vídeos curtos (um por tópico), sequência de stories, carrossel do tema principal, e-mail com o ponto mais importante |
| Artigo ou post longo | Carrossel, vídeo curto de dica, post de texto com a tese, newsletter |
| Vídeo curto que foi bem | Legenda mais profunda, post de texto com o tema, carrossel aprofundando |

## Adaptação por plataforma

- **Instagram:** visual, identidade, comunidade.
- **LinkedIn:** reflexão profissional, resultado, posição clara.
- **TikTok:** rápido, entretenimento, informal.
- **YouTube Shorts:** educativo, demonstrativo, série.
- **WhatsApp e e-mail:** direto, como conversa com quem recebe.

O mesmo trecho muda de ângulo, tom e formato em cada lugar.

## Regras

- **Nada inventado.** Citação, número e história saem da peça. Se precisar de contexto externo, marque "precisa conferir".
- **Sem regra de quantidade.** Não existe número certo de cortes por hora: conte o que achou.
- **Terceiros:** falas de convidados e dados de pessoas citadas na peça pedem autorização. Marque no plano "precisa de autorização" e ofereça contar sem identificar a pessoa, se ela concordar.
- **Minutagem real.** Toda minutagem do plano, inclusive a do que ficou de fora, sai da saída do script ou da transcrição.
- **Sem publicar:** esta skill não posta, não agenda e não corta nada.

## Formato de entrega

```
# Plano de reaproveitamento: <título da peça>

Origem: <tipo, duração ou tamanho>  |  Objetivo: <objetivo>  |  Plataformas: <lista>

## Trechos escolhidos

| Id | Minutagem | Duração | Por que funciona | Se sustenta sozinho? |
|---|---|---|---|---|

Citação de cada trecho (do script):
T1: "<texto exato>"

## Plano de derivados

| Trecho | Derivado | Plataforma | Abertura sugerida | Precisa de |
|---|---|---|---|---|

## O que deixei de fora e por quê
<uma linha por item relevante>

Próximo passo: <aprovar derivados e quem produz: roteiro com a Cami, corte com o Cortez>
```

## Outro sistema operacional

O único script é `scripts/conferir_trechos.py`, em Python 3 só com biblioteca padrão. Adapte o que for preciso e conte à pessoa o que realmente testou.

- **Python:** `python3` no macOS e Linux; `py -3` ou `python` no Windows. Sem Python, peça autorização para instalar pelo gerenciador oficial (Homebrew, winget, apt). Se não for possível, faça o plano sem o script e avise que as citações e minutagens não foram conferidas por máquina.
- **Instalar:** no Windows, copie esta pasta, sem o `install.sh`, para `%USERPROFILE%\.claude\skills\omnx-social-reaproveitar-conteudo`. No Mac e no Linux, rode o `install.sh`.
- **Caminhos:** `~` é a pasta do usuário; no Windows é `%USERPROFILE%`. Caminho com espaço vai entre aspas.
- **Abrir um arquivo salvo para a pessoa:** `open` (macOS), `start ""` (Windows), `xdg-open` (Linux).

## Outra ferramenta (Codex e outras)

Esta skill foi feita e testada no Claude Code. **Não foi testada no Codex.** Se a pessoa pedir para instalar em outra ferramenta, a IA dela adapta na hora e conta o que realmente funcionou:

- **Onde pôr os arquivos:** confira na documentação atual da ferramenta. No Codex, a referência em 08/11/2026 era `~/.agents/skills/<name>`.
- **Caminhos:** `scripts/...` é relativo à pasta onde este `SKILL.md` ficou instalado.
- **Sem executar scripts:** siga como no caso "sem Python" acima.
