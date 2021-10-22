from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from random import randint


# ***********************************************
# Тут будут методы и функции
def setup_horse():
    global state01, state02, state03, state04
    global weather, timeday
    global wincoff01, wincoff02, wincoff03, wincoff04
    global play01, play02, play03, play04
    global reverse01, reverse02, reverse03, reverse04
    global fastspeed01, fastspeed02, fastspeed03, fastspeed04

    weather = randint(1,5)
    timeday = randint(1,4)

    state01 = randint(1,5)
    state02 = randint(1, 5)
    state03 = randint(1, 5)
    state04 = randint(1, 5)

    wincoff01 = int(100 + randint(1, 30 + state01 * 70)) / 100
    wincoff02 = int(100 + randint(1, 30 + state02 * 70)) / 100
    wincoff03 = int(100 + randint(1, 30 + state03 * 70)) / 100
    wincoff04 = int(100 + randint(1, 30 + state04 * 70)) / 100

    # Маркеры ситуаций
    reverse01 = False
    reverse02 = False
    reverse03 = False
    reverse04 = False

    play01 = True
    play02 = True
    play03 = True
    play04 = True

    fastspeed01 = False
    fastspeed02 = False
    fastspeed03 = False
    fastspeed04 = False

# метод отображения выигрыша или проигрыша раунда
def win_round(horse):
    global x01, x02, x03, x04, money
    res = "И первый к финишу приходит "
    if horse == 1:
        res += namehorse01
        win = summ01.get() * wincoff01
    elif horse == 2:
        res += namehorse02
        win = summ02.get() * wincoff02
    elif horse == 3:
        res += namehorse03
        win = summ03.get() * wincoff03
    elif horse == 4:
        res += namehorse04
        win = summ04.get() * wincoff04

    if horse > 0:
        res += f"! Вы выиграли {int(win)} {valuta}."
        if win > 0:
            res += "Поздравляем! Средства уже зачислены на Ваш счет!"
            inserttext(f"Этот забег принес Вам {int(win)} {valuta}.")
        else:
            res += "К сожаленю вы проиграли"
            inserttext("Сделайте ставку, вы должны отыграться!")
        messagebox.showinfo("Результат", res)
    else:
        messagebox.showinfo("Все плохо", "До финиша никто не дошел. Забег считается несостоявшимся.")
        inserttext("Забег признан не действительным, средства списаны не будут")
        win = summ01.get() + summ02.get() + summ03.get() + summ04.get()

    money += win
    write_file(int(money))
    # сброс переменных
    setup_horse()
    # сбрасываем виджеты
    startbutton["state"] = "normal"
    stavka1["state"] = "readonly"
    stavka2["state"] = "readonly"
    stavka3["state"] = "readonly"
    stavka4["state"] = "readonly"
    stavka1.current(0)
    stavka2.current(0)
    stavka3.current(0)
    stavka4.current(0)
    # сброс позиций лошади
    x01 = 20
    x02 = 20
    x03 = 20
    x04 = 20
    horseplaceinwindow()
    # Обнавляем интерфейс
    refreshcombo(eventObject="")  # обновляем выпадающие списки и чекбоксы
    view_weahter()  # Выводим данные о погоду
    health_horse()  # Выводим показатель лошади
    inserttext(f"Ваши средства: {int(money)} {valuta}.")  # выводим имеющиеся средства на счету
    if money < 1:
        messagebox.showinfo("Стоп!", "Без денег тут не место!")


# метод отображения здоровья лошадей
def get_health():
    inserttext(health_horse(namehorse01, state01, wincoff01))
    inserttext(health_horse(namehorse02, state02, wincoff02))
    inserttext(health_horse(namehorse03, state03, wincoff03))
    inserttext(health_horse(namehorse04, state04, wincoff04))


def health_horse(name, state, win):
    s = f"Лошадь {name} "
    if state == 5:
        s += "мучается несварением желудка."
    elif state == 4:
        s += "плохо спала."
    elif state == 3:
        s += "чувствует себя хорошо."
    elif state == 2:
        s += "выспалась, готова к забегу."
    elif state == 1:
        s += "полна сил и надежд."
    s += f" ({win}:1)"
    return s


# метод отображения погоды
def view_weahter():
    s = "Сейчас на ипподроме "
    if timeday == 1:
        s += "утро, "
    elif timeday == 2:
        s += "день , "
    elif timeday == 3:
        s += "вечер, "
    elif timeday == 4:
        s += "ночь, "

    if weather == 1:
        s += "льёт сильный дождь."
    elif weather == 2:
        s += "моросит дождь."
    elif weather == 3:
        s += "облачно, на горизонте тучи."
    elif weather == 4:
        s += "безоблачно, ветренно."
    elif weather == 5:
        s += "безоблачно, прекрасная погодка."
    inserttext(s)


def runhorse():
    global money
    startbutton["state"] = "disabled"
    stavka1["state"] = "disabled"
    stavka2["state"] = "disabled"
    stavka3["state"] = "disabled"
    stavka4["state"] = "disabled"
    money -= summ02.get() + summ03.get() + summ01.get() + summ04.get()
    movehorse()


def horse_problem():
    global reverse01, reverse02, reverse03, reverse04
    global play01, play02, play03, play04
    global fastspeed01, fastspeed02, fastspeed03, fastspeed04

    # Выбираем лошадь
    horse = randint(1, 4)
    # Чем выше число, тем меньше шанс случайного события
    maxrand = 10000

    if horse == 1 and x01 > 0 and play01 == True:
        if randint(0, maxrand) < state01 * 5:
            reverse01 = not reverse01
            messagebox.showinfo("Ааааааа!", f"Лошадь {namehorse01} развернулась и бежит в обратную сторону!")
        elif randint(0, maxrand) < state01 * 5:
            play01 = False
            messagebox.showinfo("Ааааааа!", f"Что за нафиг, лошадь {namehorse01} заржала и сбросила с себя жакея!")
        elif randint(0, maxrand) < state01 * 5 and not fastspeed01:
            messagebox.showinfo("Невероятно!", f"Лошадь {namehorse01} перестала притворяться и рванула вперёд!")
            fastspeed01 = True

    if horse == 2 and x02 > 0 and play02 == True:
        if randint(0, maxrand) < state02 * 5:
            reverse02 = not reverse02
            messagebox.showinfo("Ааааааа!", f"Лошадь {namehorse02} развернулась и бежит в обратную сторону!")
        elif randint(0, maxrand) < state02 * 5:
            play02 = False
            messagebox.showinfo("Ааааааа!", f"Что за нафиг, лошадь {namehorse02} заржала и сбросила с себя жакея!")

    if horse == 3 and x03 > 0 and play03 == True:
        if randint(0, maxrand) < state03 * 5:
            reverse03 = not reverse03
            messagebox.showinfo("Ааааааа!", f"Лошадь {namehorse03} развернулась и бежит в обратную сторону!")
        elif randint(0, maxrand) < state03 * 5:
            play03 = False
            messagebox.showinfo("Ааааааа!", f"Что за нафиг, лошадь {namehorse03} заржала и сбросила с себя жакея!")

    if horse == 4 and x04 > 0 and play04 == True:
        if randint(0, maxrand) < state04 * 5:
            reverse04 = not reverse04
            messagebox.showinfo("Ааааааа!", f"Лошадь {namehorse04} развернулась и бежит в обратную сторону!")
        elif randint(0, maxrand) < state04 * 5:
            play04 = False
            messagebox.showinfo("Ааааааа!", f"Что за нафиг, лошадь {namehorse04} заржала и сбросила с себя жакея!")


def movehorse():
    global x01, x02, x03, x04

    if randint(0, 100) < 20:
        horse_problem()

    speed01 = (randint(1, timeday + weather) + randint(1, int((7 - state01)) * 3)) / randint(10, 175)
    speed02 = (randint(1, timeday + weather) + randint(1, int((7 - state02)) * 3)) / randint(10, 175)
    speed03 = (randint(1, timeday + weather) + randint(1, int((7 - state03)) * 3)) / randint(10, 175)
    speed04 = (randint(1, timeday + weather) + randint(1, int((7 - state04)) * 3)) / randint(10, 175)

    multiple = 1.5
    speed01 *= int(randint(1, 2 + state01) * (1 + fastspeed01 * multiple))
    speed02 *= int(randint(1, 2 + state02) * (1 + fastspeed02 * multiple))
    speed03 *= int(randint(1, 2 + state03) * (1 + fastspeed03 * multiple))
    speed04 *= int(randint(1, 2 + state04) * (1 + fastspeed04 * multiple))

    if play01:
        if not reverse01:
            x01 += speed01
        else:
            x01 -= speed01
    if play02:
        if not reverse02:
            x02 += speed02
        else:
            x02 -= speed02
    if play03:
        if not reverse03:
            x03 += speed03
        else:
            x03 -= speed03
    if play04:
        if not reverse04:
            x04 += speed04
        else:
            x04 -= speed04

    horseplaceinwindow()
    if (x01 < 952 and
            x02 < 952 and
            x03 < 952 and
            x04 < 952):
        root.after(5, movehorse)


# Расположение начальной позиции лошадей
def horseplaceinwindow():
    horse01.place(x=int(x01), y=20)
    horse02.place(x=int(x02), y=100)
    horse03.place(x=int(x03), y=180)
    horse04.place(x=int(x04), y=260)


def inserttext(s):
    textdiary.insert(INSERT, s + "\n")
    textdiary.see(END)


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
        print("Ошибка создания файла")
        quit()


def getvalues(summa):
    value = []
    if summa > 9:
        for i in range(0, 11):
            value.append(i * (int(summa) // 10))
    else:
        value.append(0)
        if summa > 0:
            value.append(summa)
    return value


def refreshcombo(eventObject):
    summ = summ01.get() + summ02.get() + summ03.get() + summ04.get()
    labelallmoney["text"] = f"У Вас на  счету: {int(money - summ)} {valuta}"

    if summ01.get() > 0:
        horse01game.set(True)
    else:
        horse01game.set(False)

    if summ02.get() > 0:
        horse02game.set(True)
    else:
        horse02game.set(False)

    if summ03.get() > 0:
        horse03game.set(True)
    else:
        horse03game.set(False)

    if summ04.get() > 0:
        horse04game.set(True)
    else:
        horse04game.set(False)

    stavka1["values"] = getvalues(int(money - summ02.get() - summ03.get() - summ04.get()))
    stavka2["values"] = getvalues(int(money - summ01.get() - summ03.get() - summ04.get()))
    stavka3["values"] = getvalues(int(money - summ02.get() - summ01.get() - summ04.get()))
    stavka4["values"] = getvalues(int(money - summ02.get() - summ03.get() - summ01.get()))

    if summ > 0:
        startbutton["state"] = "normal"
    else:
        startbutton["state"] = "disabled"


# ***********************************************
root = Tk()
# ***********************************************
# Тут будут переменные
x01 = 20
x02 = 20
x03 = 20
x04 = 20
valuta = 'рублей'
defaultMoney = 10000
money = 0
namehorse01 = "Жеребец"
namehorse02 = "Скакун"
namehorse03 = "Коронка"
namehorse04 = "Скайлайн"
# погода 1 - ливень, 5 - безоблачно
weather = randint(1, 5)
# день, утро, вечер, ночь
timeday = randint(1, 4)
# Зададим состояние лошадей 1 - гуд , 5 - оч плохо
state01 = randint(1, 5)
state02 = randint(1, 5)
state03 = randint(1, 5)
state04 = randint(1, 5)
# Коэффицент выигрыша
wincoff01 = int(100 + randint(1, 30 + state01 * 70)) / 100
wincoff02 = int(100 + randint(1, 30 + state02 * 70)) / 100
wincoff03 = int(100 + randint(1, 30 + state03 * 70)) / 100
wincoff04 = int(100 + randint(1, 30 + state04 * 70)) / 100
# Переменные для случайных событий
reverse01 = False
reverse02 = False
reverse03 = False
reverse04 = False
play01 = True
play02 = True
play03 = True
play04 = True
fastspeed01 = False
fastspeed02 = False
fastspeed03 = False
fastspeed04 = False
# ***********************************************
WIDTH = 1024
HIGHT = 600
# Координаты для размещения окна
POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HIGHT // 2
# Устанавливаем широту, выосту и позицию по центру
root.geometry(f"{WIDTH}x{HIGHT}+{POS_X}+{POS_Y}")
# Заголовок
root.title("ИППОДРОМ")
# Запрет на изменение окна
root.resizable(False, False)

road_image = PhotoImage(file="media/road.png")  # Загружаем изоображение
road = Label(root, image=road_image)  # Устанавливаем в Label
road.place(x=0, y=17)  # Выводим в окно

horse01_image = PhotoImage(file="media/horse01.png")
horse01 = Label(root, image=horse01_image)

horse02_image = PhotoImage(file="media/horse02.png")
horse02 = Label(root, image=horse02_image)

horse03_image = PhotoImage(file="media/horse03.png")
horse03 = Label(root, image=horse03_image)

horse04_image = PhotoImage(file="media/horse04.png")
horse04 = Label(root, image=horse04_image)

horseplaceinwindow()

# Добавление кнопки СТАРТ
startbutton = Button(text="СТАРТ", font="timesnewroman 20 bold", background="#37AA37", width=61)
startbutton.place(x=20, y=370)
startbutton["state"] = "disabled"
# Добавление текстового окна
textdiary = Text(width=70, height=8, wrap=WORD)
textdiary.place(x=430, y=450)

# Добавление "скролл" полосы
scroll = Scrollbar(command=textdiary.yview, width=20)
scroll.place(x=990, y=450, height=132)
textdiary["yscrollcommand"] = scroll.set

money = readFile()
labelallmoney = Label(text=f"Осталось средств: {money} {valuta}", font="timesnewroman 12")
labelallmoney.place(x=20, y=565)

if money <= 0:
    messagebox.showinfo(title="Стоп!", message="Без денег ты нам не нужен!")
    quit(0)

labalhorse01 = Label(text="Ставка на лошадь №1")
labalhorse01.place(x=20, y=450)

labalhorse02 = Label(text="Ставка на лошадь №2")
labalhorse02.place(x=20, y=480)

labalhorse03 = Label(text="Ставка на лошадь №3")
labalhorse03.place(x=20, y=510)

labalhorse04 = Label(text="Ставка на лошадь №4")
labalhorse04.place(x=20, y=540)
# Создание чекбоксов для выбора лошади
horse01game = BooleanVar()
horse01game.set(0)
horse01check = Checkbutton(text=namehorse01, variable=horse01game, onvalue=1, offvalue=0)
horse01check["state"] = "disabled"
horse01check.place(x=150, y=448)

horse02game = BooleanVar()
horse02game.set(0)
horse02check = Checkbutton(text=namehorse02, variable=horse02game, onvalue=1, offvalue=0)
horse02check["state"] = "disabled"
horse02check.place(x=150, y=478)

horse03game = BooleanVar()
horse03game.set(0)
horse03check = Checkbutton(text=namehorse03, variable=horse03game, onvalue=1, offvalue=0)
horse03check["state"] = "disabled"
horse03check.place(x=150, y=508)

horse04game = BooleanVar()
horse04game.set(0)
horse04check = Checkbutton(text=namehorse04, variable=horse04game, onvalue=1, offvalue=0)
horse04check["state"] = "disabled"
horse04check.place(x=150, y=538)

# Создаем выпадающий список
stavka1 = ttk.Combobox(root)
stavka2 = ttk.Combobox(root)
stavka3 = ttk.Combobox(root)
stavka4 = ttk.Combobox(root)
# Распологаем выпадающий список
stavka1["state"] = "readonly"
stavka1.place(x=280, y=450)

stavka2["state"] = "readonly"
stavka2.place(x=280, y=480)

stavka3["state"] = "readonly"
stavka3.place(x=280, y=510)

stavka4["state"] = "readonly"
stavka4.place(x=280, y=540)
# присваемваем переменной целочисленное значение
summ01 = IntVar()
summ02 = IntVar()
summ03 = IntVar()
summ04 = IntVar()
# помещаем данные метода в чекбокс
stavka1["textvariable"] = summ01
stavka2["textvariable"] = summ02
stavka3["textvariable"] = summ03
stavka4["textvariable"] = summ04
# метод, срабатывающий при выборе чекбокса
stavka1.bind("<<ComboboxSelected>>", refreshcombo)
stavka2.bind("<<ComboboxSelected>>", refreshcombo)
stavka3.bind("<<ComboboxSelected>>", refreshcombo)
stavka4.bind("<<ComboboxSelected>>", refreshcombo)

refreshcombo("")
# начальное значение в списке
stavka1.current(0)
stavka2.current(0)
stavka3.current(0)
stavka4.current(0)

# Удалить
stavka1.current(1)
refreshcombo("")
startbutton["command"] = runhorse

# Выводим текст о погоде и здоровье лошадей в чат
view_weahter()
get_health()
# Выводим главное окно на экран
root.mainloop()
