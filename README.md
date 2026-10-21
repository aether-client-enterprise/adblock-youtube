\# ytadblock



Executor que bloqueia anuncios do youtube redirecionando dominios de anuncio para 127.0.0.1 no arquivo hosts do windows.



\## pasta

C:\\Users\\joilton\\ytadblock\\



\## arquivos

\- yt\_adblock.py — executavel python

\- blocklist.txt — lista de dominios (sincronizada com o github)



\## passo a passo git



1\. abra powershell na pasta:

&#x20;  cd C:\\Users\\joilton\\ytadblock



2\. inicie o repositorio:

&#x20;  git init



3\. adicione os arquivos:

&#x20;  git add yt\_adblock.py blocklist.txt README.md



4\. faça o primeiro commit:

&#x20;  git commit -m "executor bloqueio anuncios youtube"



5\. vincule ao seu repositorio remoto (troque SEU\_USUARIO e SEU\_REPO):

&#x20;  git remote add origin https://github.com/SEU\_USUARIO/SEU\_REPO.git

&#x20;  git branch -M main

&#x20;  git push -u origin main



6\. edite GITHUB\_RAW dentro de yt\_adblock.py com o link raw do seu blocklist.txt no github, faça commit e push novamente.



\## executar local

abra o powershell como administrador e rode:



&#x20;  python yt\_adblock.py



o script grava 127.0.0.1 nos dominios de anuncio no arquivo hosts e sincroniza a blocklist do seu raw do github.

pronto. estão salvos em C:\\Users\\joilton\\ytadblock\\. agora você sobe para o github e edita o GITHUB\_RAW com o link raw do seu repositorio.

