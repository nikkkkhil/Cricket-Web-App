from pycricbuzz import Cricbuzz

c = Cricbuzz()
commentary1 = []
current_game3 = {}
matches = c.matches()
for match in matches:
    if match['mchstate'] != 'nextlive':
            col= (c.commentary(match['id']))
            for my_str in col['commentary']:
                current_game3["commentary2"] = my_str
for comment in commentary1:
    a = comment['commentary2'].replace('<br/>', '\n')
    commentary1.append(a)
    current_game3 = {}
    print(commentary1)
