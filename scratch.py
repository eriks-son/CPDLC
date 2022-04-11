import requests

departure = 'KEWR'
arrival = 'KBOS'

attempt = requests.get(f'https://5n1v87j7va.execute-api.us-east-1.amazonaws.com/Prod/route?from={departure[1:]}&to={arrival[1:]}')
route_list = attempt.json()['body']['routes']
for index in range(len(route_list)):
    print(f"Route {index + 1}:\n{route_list[index]['route']}")

attempt = requests.get(f'https://datis.clowd.io/api/{departure}')
atis = attempt.json()[0]['datis']
print(atis)
before, middle, after = atis[14:].partition("DEP") # 14: is used so that ARR/DEP at the beginning of some ATISes are not caught
found_digit = False
departing_runway = ""
arrival_runway = ""
for x in range(len(before) - 1, 0, -1):
    if before[x].isdigit():
        found_digit = True
        arrival_runway = before[x] + arrival_runway
    elif found_digit:
        break

found_digit = False
for x in after:
    if x.isdigit():
        found_digit = True
        departing_runway += x
    elif found_digit:
        break

print(f'The departing runway of {departure} is {departing_runway}\nThe arrival runway is {arrival_runway}')
