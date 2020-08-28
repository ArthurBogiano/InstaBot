# InstaBot
Bot de comentários no instagram, usando selenium python

## Usage

[INSTABOT] >> **add**    ->    Adiciona nova conta

[INSTABOT] >> **del**    ->    Deleta conta pelo "id"

[INSTABOT] >> **list**    ->    Lista contas cadastradas e "id" correspondente

[INSTABOT] >> **go**    ->    Inicia configuração da sessão

**Comandos de marcação:**

[INSTABOT] >> **marc add**    ->    Adiciona nova marcação

[INSTABOT] >> **marc del**    ->    Deleta marcação pelo "id"

[INSTABOT] >> **marc list**    ->    Lista marcações cadastradas e "id" correspondente

## Configuração de sessão

Uma sessão funciona da seguinte forma:

> O bot vai percorrer sobre todas as contas cadastradas, comentando **x** vezes **y** comentarios e curtindo a publicação.


**Url do post**  ->  URL alvo do bot, onde serão executadas as ações.  Ex: https://www.instagram.com/p/BxloJsyAhCD/

**Quantidade de voltas**  ->  Quantas vezes o bot vai repetir a fila de contas. 

**Quantidade de comentários por usuário**  ->  Quantos vezes cada conta vai comentar algo predefinido por você. 

**Texto dos comentários**  ->  Texto que vai ser comentado no post. 

- Se digitar "@", o bot vai marcar as demais contas cadastradas nos comentários aleatóriamente  
- Se digitar "@@", o bot vai marcar as marcações cadastradas nos comentários aleatóriamente  
- Se digitar "@@@", o bot vai marcar as demais contas e também as marcações cadastradas nos comentários aleatóriamente  

**Timeout**  ->  Tempo de espera (em segundos) após cada onda de comentários de cada conta. Default: 0
