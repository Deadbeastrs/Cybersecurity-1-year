# Primeiro projeto IAA

Este projeto foi desenvolvido para a cadeira de Identificação, Autenticação e Autorização ano letivo 2021/2022 por:

- José Costa 92996
- Guilherme Pereira 93134

## Setup do projeto

### Bibliotecas necessárias
Para poder correr o projeto é necessário algumas bibliotecas que podem ser instaladas usando o ficheiro de requesitos:

```bash
$ pip install -r requirements.txt
$ apt install sqlite3

```

A versão de python que foi utilizada foi a 3.8.8.

### Correr o servidor

Para correr os serviços deve-se utilizar o seguinte comando no neste diretório

```bash
$ flask run
```

### Utilização do projeto

Para verificar o funcionamento do projeto po de se fazer apartir de um browse no URL "127.0.0.1:5000", no entanto também foi disponibilizado um script que gera um numero escolhido de bots para jogar os jogos.

![Pagina inicial](https://github.com/GuilhermeP333/Projeto_IAA_oauth/raw/master/readme_images/game_selection.png)

Nesta Pagina é possivel escolher um jogo dando uma gamer tag temporaria, e também e possivel escolher as preferencias do utilizador.
Após ter carregado no botão para iniciar o jogo, se o utilizador não estiver logado então antes de dar autorização ao Cliente (TM) para este poder buscar os indicadores granulados assim como poder dar update aos indicadores,
 é pedido para que o mesmo fasso log in.

![Login](https://github.com/GuilhermeP333/Projeto_IAA_oauth/raw/master/readme_images/login.png)

![Autorização](https://github.com/GuilhermeP333/Projeto_IAA_oauth/raw/master/readme_images/auth.png)

Aṕos este processo, o jogador fica a espera de entrar numa sala, até haver jogadores suficientes para o jogo poder proceder.

![Espera](https://github.com/GuilhermeP333/Projeto_IAA_oauth/raw/master/readme_images/waiting.png)

Aṕos a sala estar cheia, isto é, haver pessoas suficientes tendo em conta as preferencias então o outcome do jogo é automaticamente gerado de forma aliatória.
Os outcomes incluiem ganhar, perder, empate, sair do jogo, batota.

![Ganhar](https://github.com/GuilhermeP333/Projeto_IAA_oauth/raw/master/readme_images/win.png)

![Perder](https://github.com/GuilhermeP333/Projeto_IAA_oauth/raw/master/readme_images/loss.png)

![Empate](https://github.com/GuilhermeP333/Projeto_IAA_oauth/raw/master/readme_images/draw.png)

Para fazer uso dos bots, para ter mais jogadores nas salas pode-se usar então o script disponibilizado bots.py. Neste scirpt e possivel atravez dos argumentos especificar o numero de bots e o numero de jogos que eles vão fazer

```
python3 bots.py numero_de_jogos numero_de_bots
```