import pyboy
import random
#
# numb = [random.randint(0,10) for o in range(10)]
#
# print(numb)
#
# print(numb[:5])
# print(numb[9:])

# def perm(l) :
# # Compute the list of all permutations of l
#     if len(l) <= 1 :
#         return [l]
#     r = []
#     for i in range(len(l)) :
#         s = l[:i] + l[i + 1 :]
#         p = perm(s)
#     for x in p :
#         r.append(l[i :i + 1] + x)
#     return r
#
#
# toto = perm("Hallo")
# print(toto)

def perm(l):
    # if len(l) <= 1:
    #     return [l]
    # r = []
    # for i in range(len(l)):
    if len(l) <= 1 :
        return [l]
    r = []
    for i in range(len(l)) :
        # s = l[:i] + l[i+1:]
        # p = perm(s)
        s = l[:i] + l[i + 1 :]
        p = perm(s)
        for x in p:
            # r.append(l[i :i + 1] + x)
            r.append(l[i :i + 1] + x)
    return (r)


toto = perm("hallo")

print(toto)