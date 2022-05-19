def cut_string(string: str, part_len: int):
    return list(string[0 + i: part_len + i] for i in range(0, len(string), part_len))
