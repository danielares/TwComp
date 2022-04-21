import re

'''
Função para limpar os tweets
Remove coisas que não são interessantes para a analise
Ou que atrapalham a analise
'''
def clean_tweet(tweet):
        tweet_clean = re.sub(r"\n", " ", tweet) # troca quebra de linha por um espaço em branco
        tweet_clean = re.sub("[^0-9A-Za-z ñÑÀàÁáÉéÍíÓóÚúÂâÊêÎîÔôÛûÃãÕõÇç@]", "", tweet_clean).lower()  # deixa somente os caracteres aceitos
        tweet_clean = re.sub(r"http\S+", "", tweet_clean)  # remove links
        tweet_clean = re.sub(r"@\S+", "", tweet_clean)  # remove @USERNAME
        #tweet_clean = re.sub(r"#\S+", "", tweet_clean)  # remove hashtags
        tweet_clean = re.sub(r"ñ", "não", tweet_clean)  # substitui ñ por não
        tweet_clean = re.sub(r"^B\S([rt]+)?", "", tweet_clean)  # remover rt do inicio dos retweets
        tweet_clean = tweet_clean.strip()
        return tweet_clean

#EMOTICONS_ALEGRIA = ['😀','😃','😄','😁','😆','😅','😂','🤣','😇','🥰','😍','😌','😋','☺️','🙃','🙂','😊',
                     #'😉','😘','😗','😙','😚','🤪','😜','😝','😛','🤑','😎','🤓','🥸','🥳','😏']
#EMOTICONS_TRISTEZA = [😐😑😒🙄😳😟😔😕🙁☹️🥺😣😖😫😩🥱😪😮‍💨😮]
#EMOTICONS_RAIVA = [😤😠😡🤬👺👹]
#EMOTICONS_NOJO = [🤢🤮]
#EMOTICONS_SURPREZA = [😱🤯😨😰😥]
#EMOTICONS_OUTROS = [👏🤲🙌👏🤝👍👎👊✊✌️]

