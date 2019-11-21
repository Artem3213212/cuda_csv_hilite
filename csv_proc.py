# from debug import snoop


def parse_csv_line(s, sep=",", quote='"'):
    """
    Parses one CSV line (by Artem)
    Gets fragments as list of 3-lists: [offset_start, offset_end, kind]
    Gets [] for incorrect line
    kind: -1 for comma, 0+ for column
    """
    if not s:
        return []
    res = []
    col, x, b = 0, 0, True
    for i, c in enumerate(s):
        if c == sep and b:
            if x != i:
                res.append([x, i, col])
                res.append([i, i + 1, -1])
            else:
                if i != 0:
                    res[-1][1] += 1
                else:
                    if x == 0:
                        res.append([0, 0, 0])
                    res.append([0, 1, -1])
            x = i + 1
            col += 1
        elif c == quote:
            b = not b
    if x != len(s):
        res.append([x, len(s), col])
    if not b:
        return []
    s = s.replace(quote * 2, "")
    i = -1
    while True:
        i = s.find(quote, i + 1)
        if i == -1:
            return res
        if not (i == 0 or s[i - 1] == sep):
            break
        i = s.find(quote, i + 1)
        if not (i == len(s) - 1 or s[i + 1] == sep):
            break
    return []

# @snoop()
def parse_csv_line_as_dict(s, sep=",", quote='"'):
    """
    Parses one CSV line
    Gets fragments as dict of lists: kind: [offset_start, offset_end]
    Gets {} for incorrect line
    """
    if not s:
        return {}
    res = {}
    col, x0, b = 0, 0, True
    for x1, c in enumerate(s):
        if c == sep and b:
            res[col] = ([x0, x1])
            x0 = x1 + 1
            col += 1
            if x1 + 1 == len(s):
                res[col] = ([x1+1, x1+1])
        elif c == quote:
            b = not b
    if x0 != len(s):
        res[col] = [x0, len(s)]
    if not b:
        return {}
    else:
        return res
    return {}


if __name__ == '__main__':
    print(parse_csv_line_as_dict('aa,,cc'))
    print(parse_csv_line_as_dict(',aa,,cc'))
    print(parse_csv_line_as_dict('"14  aa",,cc,'))
