import re


# with open('../ads.csv') as f:
#     while True:
#         try:
#             line = next(f)
#
#         # for item in line:
#         #     print(line)
#         #     result: int = re.search(r"\S,П", line)
#         #     print(result)
#                 # print(line[match.start()+1:match.end()-1)])
#             # res = re.finditer(r"\S,\S", line)
#             # print(line[res.start()+1:res.end()-1])
#             # print(list(res))
#             print(re.search(",", re.split(r"\S,\S", line)))
#         except StopIteration:
#             break
#             # print(line)
# """"""

line = """1,"Сибирская котята, 3 месяца",Павел,2500,"Продаю сибирских котят, возвраст 3 месяца."""
# # for n in
# result = re.search(r"\S,П", line)
# print(result)
# print(result.start())
# start = result.start()
# end = result.end()
# print('start', start, ', end', end, ' result:', line[start+1:end-1])
#
# result = re.finditer(r"\S,\S", line)
# print(list(result))

massiv = []
p = re.compile("\S,\S")
old = 0
for m in p.finditer(line):
    massiv.append(line[old:m.start()+1])
    old = m.start()+2
    # print(m.start()+0, m.group())
print(massiv)
