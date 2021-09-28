import time

DECIMALS = 10 ** 9


def get_token_change(index: int, post_balance, pre: list):
    for i in pre:
        if i['accountIndex'] == index:
            pre_balance = int(i['uiTokenAmount']['amount']) / 10 ** i['uiTokenAmount']['decimals']
            return post_balance - pre_balance
    return post_balance


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
    if not pre:
        for i in range(len(post)):
            amount = post[i]['uiTokenAmount']['uiAmount']
            result.append(
                (accounts[post[i]['accountIndex']], post[i]['mint'], amount, amount))
        return result

    if len(post) > len(pre):
        for i in range(len(post)):
            post_balance = int(post[i]['uiTokenAmount']['amount']) / 10 ** post[i]['uiTokenAmount']['decimals']
            change = get_token_change(post[i]['accountIndex'], post_balance, pre)
            if change != 0:
                result.append(
                    (accounts[post[i]['accountIndex']], post[i]['mint'], post_balance, change))
        return result

    for i in range(len(post)):
        post_balance = int(post[i]['uiTokenAmount']['amount']) / 10 ** post[i]['uiTokenAmount']['decimals']
        pre_balance = int(pre[i]['uiTokenAmount']['amount']) / 10 ** pre[i]['uiTokenAmount']['decimals']
        change = post_balance - pre_balance
        if change != 0:
            result.append(
                (accounts[post[i]['accountIndex']], post[i]['mint'], post[i]['uiTokenAmount']['uiAmount'], change))
    return result


def timestamp(block_time):
    return time.ctime(block_time)
