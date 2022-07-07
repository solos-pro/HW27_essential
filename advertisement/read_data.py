import re

with open('ads.csv') as f:
    pre_ = []
    while True:
        try:
            line = str(next(f))
            red_line = []
            p = re.compile(r"\S,\S")
            # p = re.compile(",")
            old = 0
            n = 0
            for m in p.finditer(line):
                n += 1
                red_line.append(line[old:m.start() + 1])
                # print(len(red_line))
                old = m.start() + 2
                if len(red_line) >= 7:
                    pre_ = red_line[:7]
                    print(pre_)
                    print(red_line)
                    del red_line[0:7]

        except StopIteration:
            break
#             # print(line)
# """"""

# line = """1,"Сибирская котята, 3 месяца",Павел,2500,"Продаю сибирских котят, возвраст 3 месяца."""
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

# massiv, pre = [], []
# p = re.compile("\S,\S")
# old = 0
# n = 0
# for m in p.finditer(line):
#     n += 1
#     massiv.append(line[old:m.start()+1])
#     old = m.start()+2
#     if len(massiv) >= 7:
#         pre = massiv[:7]
#     # print(m.start()+0, m.group())
# print(massiv)
