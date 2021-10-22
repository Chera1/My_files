from ctypes import *
import time
import random

windll.Kernel32.GetStdHandle.restype = c_ulong
h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))


# Установка цвета текста
def color(c):
    windll.Kernel32.SetConsoleTextAttribute(h, c)


money = 0
defaultMoney = 10000
summaWin = 0
summaLose = 0
valuta = 'руб'
playGame = True


def main():
    global money, playGame

    money = readFile()
    start_money = money
    while playGame and money > 0:
        getPrivet(7, "Приветствуем тебя в нашем казино! Проходи присаживайся!")
        color(14)
        print(f"У тебя на счету {money} {valuta}лей")
        color(6)
        print("Ты можешь сыграть в:\n"
              "1. Рулетку\n"
              "2. Кости\n"
              "3. Однорукого бандита\n"
              "0. Выход. Ставка 0 в играх - выход.")
        color(7)

        user = getInput("1,2,3,0", "Твой выбор? ")

        if user == "0":
            print("Вы покидаете наше казино! Всего доброго!")
            playGame = False
        elif user == "1":
            roulette()
        elif user == "2":
            dice()
        elif user == "3":
            oneHandBandit()
    getPrivet(12, "Жаль, что ты покидаешь нас!")
    color(13)
    if money < 0:
        print("Упс , у тебя закончились деньги")

    color(11)
    if money > start_money:
        print(f"При старте игры у тебя было {start_money}\n"
              f"Чтож, ты хорошо поиграл, ты выиграл {money - start_money} {valuta}лей.\n"
              f"возвращайся и приумножай свое состояние")
    elif money == start_money:
        print("Ничего себе! У тебя осталось столько же денег, сколько и было. И не выиграл и не проиграл!")
    else:
        print(f"К сожалению ты проиграл {start_money - money} {valuta}лей.\n"
              f"Но ты не огорчайся, обязательно еще повезёт")
    write_file(money)
    color(7)
    quit()


def roulette():
    global money
    playGame = True

    while playGame and money > 0:
        getPrivet(11, "ДОБРО ПОЖАЛОВАТЬ НА ИГРУ В РУЛЕТКУ!")
        print(f"У тебя на счету {money} {valuta}лей")
        print("Ставлю на...\n"
              "    1. Четное (выигрыш 1:1)\n"
              "    2. Нечетное (выигрыш 1:1)\n"
              "    3. Дюжина (выигрыш 3:1)\n"
              "    4. Число (выигрыш 36:1)\n"
              "    0. Возврат в предыдущее меню")
        user = getInput("0,1,2,3,4", "Твой выбор? ")
        playroulette = True
        if user == "1":
            pass  # На четное
        elif user == "2":
            pass  # На нечетное
        elif user == "3":
            color(2)
            print()
            print("Выберите диапазон: \n"
                  "    1. От 0 до 12\n"
                  "    2. От 13 до 24 \n"
                  "    3. От 25 до 36\n"
                  "    0. Назад")

            dujina = getInput("0,1,2,3", "Твой выбор? ")
            if dujina == "1":
                textduzina = "от 0 до 12"
            elif dujina == "2":
                textduzina = "от 13 до 24"
            elif dujina == "3":
                textduzina = "от 25 до 36"
            elif dujina == "0":
                playroulette = False
        elif user == "4":
            chislo = getIntInput(0, 36, "Выберите число от 0 до 36: ")
        # Выход с рулетки
        color(7)
        if user == "0":
            return 0

        if playroulette:
            stavka = getIntInput(0, money, f"Введите ставку(не больше {money} {valuta}лей): ")
            if stavka == 0:
                return 0

            number = getRoulette(True)
            print()
            color(11)
            print(f"    Выпало число {number} " + "*" * number)
            if number == 37:
                print("    Выпало число 00" + "*" * 37)
            if number == 38:
                print("    Выпало число 00" + "*" * 38)
            if user == "1":
                print("    Ты ставил на ЧЕТНОЕ!")
                if number % 2 == 0 and number < 37:
                    money += stavka
                    Win(stavka)
                    write_file(money)
                else:
                    money -= stavka
                    Lose(stavka)
                    write_file(money)
            elif user == "2":
                print("    Ты ставил на НЕЧЕТНОЕ!")
                if number % 2 == 0 and number < 37:
                    money -= stavka
                    Lose(stavka)
                    write_file(money)
                else:
                    money += stavka
                    Win(stavka)
                    write_file(money)
            elif user == "3":
                print(f"    Ставка сделана на диапозон числа {textduzina}.")
                windujina = ""
                if number < 13:
                    windujina = "1"
                elif 12 < number < 25:
                    windujina = "2"
                elif 25 < number < 37:
                    windujina = "3"

                if dujina == windujina:
                    money += stavka * 2
                    Win(stavka * 3)
                    write_file(money)
                else:
                    money -= stavka
                    Lose(stavka)
                    write_file(money)
            elif user == "4":
                print(f"    Ты ставил на {chislo}!")
                if chislo == number:
                    money += stavka * 35
                    stavka *= 36
                    Win(stavka)
                    write_file(money)
                else:
                    money -= stavka
                    Lose(stavka)
                    write_file(money)
            print()
            input("Нажмите Enter чтобы продолжить....")


def getRoulette(visible):
    tickTime = random.randint(100, 200) / 10000
    mainTime = 0
    number = random.randint(0, 38)
    increaseTickTime = random.randint(100, 110) / 100
    col = 1
    while mainTime < 0.5:
        col += 1
        if col == 15:
            col = 1
            mainTime += tickTime
            tickTime += increaseTickTime
        color(col)
        number += 1
        if number > 38:
            number = 0
            print()
        printNumber = number
        if printNumber == 37:
            printNumber = "00"
        elif printNumber == 38:
            printNumber = "000"
        print(" Число >",
              printNumber,
              "*" * number,
              " " * (79 - number * 2),
              "*" * number)
        # Delaem pause
        if visible:
            time.sleep(mainTime)
    return number


def dice():
    global money
    playGame = True

    while playGame:
        getPrivet(11, "ДОБРО ПОЖАЛОВАТЬ НА ИГРУ В КОСТИ!")
        color(14)
        print(f"\n    У тебя на счету {money} {valuta}лей\n")
        color(7)
        stavka = getIntInput(0, money, f"    Сделай ставку в пределах {money} {valuta}лей: ")

        if stavka == 0:
            return 0

        playRound = True
        control = stavka
        oldResult = getDice()
        firstPlay = True

        while playRound and money > 0 and stavka > 0:
            if stavka > money:
                stavka = money
            color(11)
            print(f"\n В твоем распоряжении {stavka} {valuta}лей.")
            print(f"\n Текущая сумма чисел на гранях равна {oldResult}")
            print(f"\n Сумма чисел на гранях будет больше, меньше или равна предыдущей?")
            x = getInput("0123", " Введи 1 - больше, 2 - меньше, 3 - равна или 0 - выход: ")

            if x != 0:
                firstPlay = False
                if stavka > money:
                    stavka = money
                money -= stavka
                diceResult = getDice()

                win = False
                if oldResult > diceResult:
                    if x == "2":
                        win = True
                elif oldResult < diceResult:
                    if x == "1":
                        win = True

                if not x == "3":
                    if win:
                        money += stavka + stavka // 5
                        Win(stavka // 5)
                        write_file(money)
                        stavka += stavka // 5
                    else:
                        stavka = control
                        Lose(stavka)
                        write_file(money)
                elif x == "3":
                    if oldResult == diceResult:
                        money += stavka * 3
                        Win(stavka * 3)
                        write_file(money)
                        stavka *= 3
                    else:
                        stavka = control
                        Lose(stavka)
                        write_file(money)

                oldResult = diceResult

            else:
                if firstPlay:
                    money -= stavka
                playRound = False


def getDice():
    count = random.randint(3, 8)
    sleep = 0
    while count > 0:
        color(count + 7)
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        print(" " * 40 + "---------")
        print(" " * 40 + "|" + f"{x}" + "|" + " |" + f"{y}" + "|")
        print(" " * 40 + "---------")
        time.sleep(sleep)
        sleep += 1 / count
        count -= 1
    return x + y


def oneHandBandit():
    global money
    playGame = True
    while (playGame):
        getPrivet(3, 'ДОБРО ПОЖАЛОВАТЬ НА ИГРУ В ОДНОРУКОГО БАНДИТА')
        color(14)
        print(f'\n У тебя на счету {money} {valuta}\n')
        color(5)
        print(" Правила игры: ")
        print('''        1. При совпадении 2-х чисел ставка не списывается.
        2. При совпадении 3-х чисел выигрыш 2:1.
        3. При совпадении 4-х чисел выигрыш 5:1.
        4. При совпадении 5-ти чисел выигрыш 10:1.
        0. Ставка 0 для завершения игры. ''')
        stavka = getIntInput(0, money, f' Введи ставку от 0 до {money}: ')
        if stavka == 0:
            return 0
        money -= stavka
        money += getOHBRes(stavka)
        if money <= 0:
            playGame = False


def getOHBRes(stavka):
    res = stavka
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 0
    getD1 = True
    getD2 = True
    getD3 = True
    getD4 = True
    getD5 = True
    col = 10
    while getD1 or getD2 or getD3 or getD4 or getD5:
        if getD1:
            d1 += 1
        if getD2:
            d2 -= 1
        if getD3:
            d3 += 1
        if getD4:
            d4 -= 1
        if getD5:
            d5 += 1
        if d1 > 9:
            d1 = 0
        if d2 < 0:
            d2 = 9
        if d3 > 9:
            d3 = 0
        if d4 < 0:
            d4 = 9
        if d5 > 9:
            d5 = 0
        if random.randint(0, 20) == 1:
            getD1 = False
        if random.randint(0, 20) == 1:
            getD2 = False
        if random.randint(0, 20) == 1:
            getD3 = False
        if random.randint(0, 20) == 1:
            getD4 = False
        if random.randint(0, 20) == 1:
            getD5 = False
        time.sleep(0.1)
        color(col)
        col += 1
        if col > 15:
            col = 10

        # Cтрока со знаком %, оформление
        print("    " + "%" * 10)
        print(f"    {d1} {d2} {d3} {d4} {d5}")

    maxCount = getMaxCount(d1, d2, d3, d4, d5)

    color(14)
    if maxCount == 2:
        print(f'  Совпадение двух чисел! Твой выигрыш в размере ставки: {res}')
    elif maxCount == 3:
        res *= 2
        print(f'  Совпадение трех чисел! Твой выигрыш 2:1: {res}')
    elif maxCount == 4:
        res *= 5
        print(f'  Совпадение четырех чисел! Твой выигрыш 5:1: {res}')
    elif maxCount == 5:
        res *= 10
        print(f'  БИНГО! Совпадение ВСЕХ чисел! Твой выигрыш 10:1: {res}')
    else:
        Lose(res)
        res = 0
    color(11)
    print()
    input(" Нажмите Enter для продолжения...")
    return res


def getMaxCount(d1, d2, d3, d4, d5):
    spisok = [d1, d2, d3, d4, d5]
    ret = {}
    for i in spisok:
        ret[i] = ret.get(i, 0) + 1
    ret = max(ret.items(), key=lambda x: x[1])
    return ret[1]


def Win(summaWin):
    color(14)
    print(f"    Победа за тобой! Выигрыш составил: {summaWin} {valuta}.")
    print(f"    У тебя на счету: {money} {valuta}")


def Lose(summaLose):
    color(12)
    print(f"    К сожалению вы проиграли: {summaLose} {valuta}лей.")
    print(f"    У тебя на счету: {money} {valuta}")
    print("    Нужно обязательно отыграться!")


# Вывод на экран заголовка
def getPrivet(c, message):
    color(c)
    for i in range(30):
        print("")
    print('*' * (len(message) + 2) + '\n' + message + '\n' + '*' * (len(message) + 2))


# Функция ввода значения
def getInput(digit, message):
    color(7)
    ret = ""
    while ret == "" or not ret in digit:
        ret = input(message)
    return ret


# Функция ввода целого числа
def getIntInput(minimum, maximum, message):
    color(7)
    ret = -1
    while ret < minimum or ret > maximum:
        st = input(message)
        if st.isdigit():
            ret = int(st)
        else:
            print("Введите целое число")
    return ret


# Чтение из файла осташийся функции
def readFile():
    try:
        f = open("money.dat", "r")
        m = int(f.readline())
        f.close()
    except FileNotFoundError:
        print(f"Файл не был найден на Ваш счет зачислено {defaultMoney} {valuta}")
        m = defaultMoney
    return m


# Запись в файл
def write_file(moneyToSave):
    try:
        f = open("money.dat", "w")
        f.write(str(moneyToSave))
        f.close()
    except:
        print("Ошибка записи в файл")
        quit()


# print(f"{getIntInput(0, 10, 'Введите число от 0 до 10 ')}")
# getPrivet('Привет, я такой типа отвлекаю')

# Последняя строчка файла
main()
