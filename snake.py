from Tkinter import *
from threading import Timer, Thread
from pynput.keyboard import Key, Listener
from random import randrange


class keyboardInput:
    lis = Listener
    vaaa = "ss"

    @staticmethod
    def on_press(key):
        # print('{0}'.format(
        #     key))
        if key == Key.up:
            mat.dir = 3
        if key == Key.down:
            mat.dir = 0
        if key == Key.left:
            mat.dir = 2
        if key == Key.right:
            mat.dir = 1
        if (key == Key.space) & (not par.playvar):
            timerstart()
            # if key == Key.esc:
            # exit()
            # return False

    # def on_release(key):
    #     print('{0}'.format(
    #         key))
    #     if key == Key.esc:
    #         # Stop listener
    #         return False

    def sluchaczguzikow(self):
        # Collect events until released
        with Listener(
                on_press=self.on_press) as listener:
            print("Start!")
            self.lis = listener
            self.lis.join()

    def deinit(self):
        self.lis.stop()

    def __init__(self):
        thr = Thread(target=self.sluchaczguzikow)
        thr.start()
        # self.sluchaczguzikow()

    pass


def closewindow():
    par.playvar = False
    ki.deinit()
    app.destroy()
    print("Press any key to end game")
    exit()


class par:
    def __init__(self):
        pass

    x = 320
    y = 320
    rozdzielczoscX = x / 32
    rozdzielczoscY = y / 32
    playvar = False
    i = 0
    seg = 10
    wielkosc_segmentu = 10
    usunKoniecWeza = True
    kolorSegmentu = "#696b39"
    kolorGlowy = "#696b39"
    kolorPapu = "black"
    kolorBack = "#c3ca22"
    tick = 0.05
    mnoznik = None


def setwindowsize(x, y):
    app.wm_minsize(x, y)
    app.wm_maxsize(x, y)


def timerstart():
    if par.playvar:
        par.playvar = False
        # btext.set("Start")
    else:
        mat.dir = 0
        par.playvar = True
        can.delete(startlabel)
        # btext.set("Stop")
        timertick()


def printtick():
    if par.playvar:
        mat.add()
        timertick()


def timertick():
    if par.playvar:
        tim = Timer(par.tick, printtick)
        tim.start()


class matrix:
    tablica = [[5, 4], [5, 3], [5, 2]]
    papu = [10, 10]
    papu_seg = None
    waz = []
    head = [5, 5]
    head_can = None
    dir = 0
    canvas = None
    punkty = None

    def __init__(self, cnv, labelpunkty):
        self.punkty = labelpunkty
        self.canvas = cnv
        self.startGame()
        pass

    def startGame(self):
        self.tablica = [[5, 4], [5, 3], [5, 2]]
        self.head = [5, 5]
        self.head_can = None
        self.generujNowePapu()
        self.waz = []
        for i in self.tablica:
            seg = self.canvas.create_rectangle(i[0] * 10, i[1] * 10, i[0] * 10 + par.seg, i[1] * 10 + par.seg,
                                               fill=par.kolorSegmentu, outline=par.kolorSegmentu)
            self.waz.insert(0, seg)
        self.printhead(self.canvas)

    def add(self):
        temp = [0, 0]
        if self.dir == 0:  # w dol
            temp = [0, 1]
        elif self.dir == 1:  # w prawo
            temp = [1, 0]
        elif self.dir == 2:  # w lewo
            temp = [-1, 0]
        elif self.dir == 3:  # w gore
            temp = [0, -1]
        self.tablica.append(self.head)
        r = self.head[0] + temp[0]
        a = self.head[1] + temp[1]
        self.head = [r, a]
        self.rysuj(self.canvas)
        self.wazTrafil(self.head)
        self.sprawdzKolizje()

    def wazTrafil(self, temp):
        # if (temp[0] == self.papu[0]) & (temp[1] == self.papu[1]):
        if temp == self.papu:
            self.wazTrafia()

    def wazTrafia(self):
        par.usunKoniecWeza = False
        self.canvas.delete(self.papu_seg)
        self.generujNowePapu()
        yyy = str(len(self.tablica) - 2)
        self.punkty.set("Wynik = " + yyy)

    def generujNowePapu(self):
        x = randrange(0, par.rozdzielczoscX)
        y = randrange(0, par.rozdzielczoscY)
        self.papu = [x, y]
        self.printpapu(self.canvas)

    def rysuj(self, cnv):
        if par.usunKoniecWeza:
            cnv.delete(self.waz[0])
            self.waz.pop(0)
            self.tablica.pop(0)
        par.usunKoniecWeza = True
        i = self.tablica[-1]
        self.printhead(cnv)
        self.printseg(cnv, i)

    def printseg(self, cnv, tab):
        i = tab
        a = par.wielkosc_segmentu
        self.waz.append(
            cnv.create_rectangle(i[0] * a, i[1] * a, i[0] * a + par.seg, i[1] * a + par.seg,
                                 fill=par.kolorSegmentu, outline=par.kolorSegmentu))

    def printpapu(self, cnv):
        a = par.wielkosc_segmentu
        i = self.papu
        self.papu_seg = cnv.create_rectangle(i[0] * a, i[1] * a, i[0] * a + par.seg, i[1] * a + par.seg,
                                             fill=par.kolorPapu, outline=par.kolorSegmentu)

    def printhead(self, cnv):
        a = par.wielkosc_segmentu
        cnv.delete(self.head_can)
        self.head_can = cnv.create_rectangle(self.head[0] * a, self.head[1] * a,
                                             self.head[0] * a + par.seg, self.head[1] * a + par.seg,
                                             fill=par.kolorGlowy, outline=par.kolorSegmentu)

    def sprawdzKolizje(self):
        for i in self.tablica:
            if self.head == i:
                self.koniecGry()
        if self.head[0] > 32:
            self.koniecGry()
        if self.head[1] > 32:
            self.koniecGry()
        if self.head[0] < 0:
            self.koniecGry()
        if self.head[1] < 0:
            self.koniecGry()

    def koniecGry(self):
        print "Game Over!"
        self.canvas.delete("all")
        self.punkty.set("Wynik = 0")
        par.playvar = False
        self.startGame()
        self.dir = 0
        print("Press space to play")


def typeSpeed():
    x = int(input("Type snake speed <1;100> : "))
    if x > 100:
        x = typeSpeed()
    if x < 1:
        x = typeSpeed()
    return x

mn = typeSpeed()
par.mnoznik = mn
par.tick = 1/float(mn)

ki = keyboardInput()

app = Tk()
app.title("Snake")
setwindowsize(par.y, par.x + 20)
zmienna = StringVar()
zmienna.set(app.winfo_height())
label = Label(app, textvariable=zmienna)
label.pack()
label.place(x=100, y=280)

# button = Button(text="Koniec", command=closewindow)
# button.place(x=0, y=par.y-25)
# btext = StringVar()
#
# button = Button(textvariable=btext, command=timerstart)
# button.place(x=par.x-80, y=par.y-25)
# btext.set("Start")

tekst = StringVar()
Label(app, width=10, textvariable=tekst).place(y=par.x + 2, x=0)

can = Canvas(app, bg=par.kolorBack, width=par.x, height=par.y)

can.pack()
tekst.set("Wynik = 0")
startlabel = can.create_text(par.x / 2, par.y / 2, text="Press Space to play", fill="black")
mat = matrix(can, tekst)
app.protocol('WM_DELETE_WINDOW', closewindow)

mainloop()

# keyboard = Controller()
# keyboard.press("A")
test content for git tutorial
