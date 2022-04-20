import requests


def get_ops(icao):
    attempt = requests.get(f'https://datis.clowd.io/api/{icao}')
    atis = attempt.json()[0]['datis']
    # 14: is used so that ARR/DEP at the beginning of some ATISes are not caught
    before, middle, after = atis[14:].partition("DEP")
    arr_runway = ""
    dep_runway = ""
    found_digit = False
    for x in range(len(before) - 1, 0, -1):
        if before[x].isdigit():
            found_digit = True
            arr_runway = before[x] + arr_runway
        elif found_digit:
            break

    found_digit = False
    for x in after:
        if x.isdigit():
            found_digit = True
            dep_runway += x
        elif found_digit:
            break

    return dep_runway, arr_runway
