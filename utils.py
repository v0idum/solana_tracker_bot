import time

DECIMALS = 10 ** 9

pre_tokens = [{'accountIndex': 4, 'mint': '4WqzbJkcrU3vnoLdAwv8XVhZPeVACzqbJiUepwYqWLmW',
               'uiTokenAmount': {'amount': '1', 'decimals': 0, 'uiAmount': 1.0, 'uiAmountString': '1'}}]

post_tokens = [{'accountIndex': 1, 'mint': '4WqzbJkcrU3vnoLdAwv8XVhZPeVACzqbJiUepwYqWLmW',
                'uiTokenAmount': {'amount': '1', 'decimals': 0, 'uiAmount': 1.0, 'uiAmountString': '1'}},
               {'accountIndex': 4, 'mint': '4WqzbJkcrU3vnoLdAwv8XVhZPeVACzqbJiUepwYqWLmW',
                'uiTokenAmount': {'amount': '0', 'decimals': 0, 'uiAmount': None, 'uiAmountString': '0'}}]


def contains(index: int, pre: list) -> bool:
    for i in pre:
        if i['accountIndex'] == index:
            return True
    return False


def to_sol(lamports: int):
    return lamports / DECIMALS


def get_balance_changes(accounts: list, pre: list, post: list):
    result = []
    for i in range(len(post)):
        change = post[i] - pre[i]
        if change != 0:
            result.append((accounts[i], to_sol(post[i]), to_sol(change)))
    return result


def get_token_balances(accounts: list, pre: list, post: list):
    if not pre and not post:
        return
    result = []
    if not pre or len(post) > len(pre):
        for i in range(len(post)):
            if not contains(post[i]['accountIndex'], pre):
                change = post[i]['uiTokenAmount']['uiAmount']
                result.append(
                    (accounts[post[i]['accountIndex']], post[i]['mint'], post[i]['uiTokenAmount']['uiAmount'], change))
        return result

    for i in range(len(post)):
        change = post[i]['uiTokenAmount']['uiAmount'] - pre[i]['uiTokenAmount']['uiAmount']
        if change != 0:
            result.append(
                (accounts[post[i]['accountIndex']], post[i]['mint'], post[i]['uiTokenAmount']['uiAmount'], change))
    return result


def timestamp(block_time):
    return time.ctime(block_time)
