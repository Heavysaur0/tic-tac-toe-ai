from random import choice


def to_binary1(tab):
    return sum(int(b)<<(len(tab)-i-1)for i,b in enumerate(tab))

def to_binary15(tab):
    return sum(1<<i for i in range(len(tab))if tab[-i-1])


def to_binary2(l):
    return int("".join(str(int(b))for b in l),2)


def to_binary3(tab):
    somme = 0
    for i in range(len(tab)):
        somme *= 2
        element = 1 if tab[i] else 0
        somme += element
    return somme

from functools import reduce

def to_binary35(l):
    return reduce(lambda a,b:2*a|b,l,0)

def somme(tab):
    return (lambda f, x: f(f, x))(lambda self, lst: (lst[0] + self(self, lst[1:])) if len(lst) else 0, tab)


def to_binary4(tab):
    somme = 0
    for i in range(len(tab)):
        if tab[i]:
            somme += 2 ** (len(tab) - i - 1)
    return somme


test = [choice([True, False]) for _ in range(10)]
print(test)
print(to_binary1(test))
print(to_binary15(test))
print(to_binary2(test))
print(to_binary3(test))
print(to_binary35(test))
print(to_binary4(test))

test = [3, 5, 10, -103, 0, 3, -5]
print(somme(test))
print(sum(test))