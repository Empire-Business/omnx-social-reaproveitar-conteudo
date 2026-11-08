# Reaproveitar conteúdo

Guia visual: abra o `COMO-FUNCIONA.html` desta pasta (dois cliques; funciona sem internet).

Lê uma peça longa que já existe (live, podcast, aula, artigo), acha os trechos que se sustentam sozinhos, confere minutagem e citação com um programa e entrega o plano de derivados por plataforma. Não escreve roteiro nem corta o vídeo.

## Como instalar

**Direto do GitHub:** no Claude Code, diga: "Instale a skill a partir de https://github.com/Empire-Business/omnx-social-reaproveitar-conteudo". Para atualizar, diga: "Atualize a skill a partir de https://github.com/Empire-Business/omnx-social-reaproveitar-conteudo". A IA baixa e copia os arquivos.

Se você já baixou esta pasta:

1. Abra o Claude Code (aplicativo do Claude, aba **Code**, ambiente **Local**).
2. Escreva: **"Instale a skill omnx-social-reaproveitar-conteudo a partir desta pasta: `<caminho desta pasta>`"**.
3. A IA copia a skill para o lugar certo. Você não digita comando nenhum e vê um aviso de que terminou.
4. Abra uma conversa nova e peça, por exemplo: **"Tenho a transcrição da minha live. Reaproveita esse conteúdo para Instagram e LinkedIn."**.

### Instalar à mão

- **Mac ou Linux:** rode `bash install.sh` nesta pasta (dá para rodar de qualquer lugar, com o caminho entre aspas). A skill vai para `~/.claude/skills/omnx-social-reaproveitar-conteudo`. Se editar algo aqui, rode de novo.
- **Windows:** copie esta pasta, sem o `install.sh`, para `%USERPROFILE%\.claude\skills\omnx-social-reaproveitar-conteudo`. Ou peça para a IA fazer isso.

## Precisa de

Python 3 (gratuito), para o programa que confere as citações. Se faltar, a IA avisa e só instala com a sua autorização.

## O que ela não faz

- Não escreve o roteiro final (Cami) nem corta o vídeo (Cortez).
- Não inventa citação, número ou história.
- Não publica nem agenda.

## Pedidos que funcionam

- "Tenho a transcrição da minha live. Reaproveita esse conteúdo para Instagram e LinkedIn."
- "O que dá para tirar desse podcast?"
- "Quais os melhores trechos dessa aula?"
- "Transforma esse artigo em conteúdo para as redes."

## Outro sistema operacional e outra ferramenta

As seções "Outro sistema operacional" e "Outra ferramenta (Codex e outras)" do `SKILL.md` dizem à IA o que adaptar. Feita e testada no Claude Code em macOS. **Não foi testada no Codex** nem no Windows e Linux: a IA da pessoa adapta ao instalar e conta o que funcionou.
