def merge_fire(rounds: list[dict]) -> list[dict]:
    # 第一步：对 0 火进行合并（5局合并为1局1火）
    merged_rounds = []
    i = 0
    while i < len(rounds):
        current = rounds[i]
        group = [current]
        j = i + 1
        while j < len(rounds) and rounds[j]["pt"] == current["pt"] and \
                rounds[j]["band_name"] == current["band_name"] and \
                rounds[j]["score_range"] == current["score_range"] and \
                rounds[j]["fire"] == current["fire"]:
            group.append(rounds[j])
            j += 1
        if current["fire"] == 0:
            count = len(group)
            num_merge = count // 5
            remainder = count % 5
            for _ in range(num_merge):
                merged_rounds.append({**current, "fire": 1})
            for _ in range(remainder):
                merged_rounds.append({**current, "fire": 0})
        else:
            merged_rounds.extend(group)
        i = j

    # 第二步：对 fire 为1的局进行合并
    final_rounds = []
    i = 0
    while i < len(merged_rounds):
        current = merged_rounds[i]
        if current["fire"] == 1:
            group = [current]
            j = i + 1
            while j < len(merged_rounds) and merged_rounds[j]["pt"] == current["pt"] and \
                    merged_rounds[j]["band_name"] == current["band_name"] and \
                    merged_rounds[j]["score_range"] == current["score_range"] and \
                    merged_rounds[j]["fire"] == 1:
                group.append(merged_rounds[j])
                j += 1
            count = len(group)
            # 优先合并3局为3火
            while count >= 3:
                final_rounds.append({**current, "fire": 3})
                count -= 3
            # 其次合并2局为2火
            while count >= 2:
                final_rounds.append({**current, "fire": 2})
                count -= 2
            # 其余保持1火
            for _ in range(count):
                final_rounds.append({**current, "fire": 1})
            i = j
        else:
            final_rounds.append(current)
            i += 1

    return final_rounds