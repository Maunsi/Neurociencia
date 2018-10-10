import random


def generadorDePares():
    with open("pairInputs.txt", "w") as f:
        for i in range(5):
            left = random.randint(1,5)
            right = random.randint(1,5)
            s = str(left) + "," + str(right)
            f.write("%s\n" % s)
    f.close


def generadorDeResultados():
    resFile = open("resInputs.txt", "w")
    with open("pairInputs.txt", "r") as f:
        lines = f.readlines()
        n = len(lines)

        for i in range(n/2):
            left, right = lines[i].split(",")
            sum = int(left) + int(right)
            resFile.write("%s\n" % str(sum))
        for i in range(n/2, n):
            left, right = lines[i].split(",")
            l = int(left)
            r = int(right)
            notSum = random.randint(1,5)
            while (notSum == (l + r) or notSum == l or notSum == r):
                notSum = random.randint(1,5)
            resFile.write("%s\n" % str(notSum))
    f.close()
    resFile.close()


if __name__ == "__main__":
    generadorDePares()
    generadorDeResultados()