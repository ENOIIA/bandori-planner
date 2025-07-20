def coin_change(coins: list[int], amount: int) -> list[int]:
    dp: list[float] = [float('inf')] * (amount + 1)
    choice: list[int] = [-1] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                choice[i] = coin

    if dp[amount] == float('inf'):
        return []  # 无法达成目标pt

    # 回溯还原组合
    plan_coins: list[int] = []
    i: int = amount
    while i > 0:
        coin: int = choice[i]
        plan_coins.append(coin)
        i -= coin
    plan_coins.reverse()
    return plan_coins
