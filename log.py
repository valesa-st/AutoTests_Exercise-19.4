from datetime import datetime
import json


def logrequests(func):
    """Логирует запросы и ответы"""

    def wrapper_log(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        value = func(*args, **kwargs)

# Открываем файл лога или создаем при его отстутствии.
        try:
            with open('log.txt', 'r', encoding='utf8') as myFile:
                txt = myFile.read()
                if 'Log file for API testing https://petfriends.skillfactory.ru/' not in txt:
                    txt = 50*'*'+'\n'+'Log file for API testing https://petfriends.skillfactory.ru/'+'\n'+50*'*'

        except:
            txt = 50*'*'+'\n'+'Log file for API testing https://petfriends.skillfactory.ru/'+'\n'+50*'*'

        try:
            with open('log.txt', 'w', encoding='utf8') as myFile:

                # time separator
                date = '\n'+'\n'+str(datetime.now())+'\n'
                txt += date+f"Function: {func.__name__}\n" \
                            f"Request params:\n{signature}\n" \
                            f"Status:\n{value[0]}\n" \
                            f"Response:\n{value[1]}\n\n"
                myFile.write(txt)

        finally:

            return value
    return wrapper_log
