import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from os import listdir
'''
path = 'figuras/'
list_image = listdir(path)
file = path + list_image[1]

image = mpimg.imread(file)
fig, ax = plt.subplots()
imgplot = ax.imshow(image)
fig.canvas.draw()
plt.draw()

def onclick(event):
    print(event)

    global ix, iy
    ix, iy = event.xdata, event.ydata
    print ('x = %d, y = %d'%(ix, iy))

    global coords
    coords = [ix, iy]

    return coords


for i in np.arange(0,1):

    cid = fig.canvas.mpl_connect('button_press_event', onclick)


plt.show()'''

import numpy as np
import matplotlib.pyplot as plt

class Click():
    def __init__(self, ax, func, button=1):
        self.ax=ax
        self.func=func
        self.button=button
        self.press=False
        self.move = False
        self.c1=self.ax.figure.canvas.mpl_connect('button_press_event', self.onpress)
        self.c2=self.ax.figure.canvas.mpl_connect('button_release_event', self.onrelease)
        self.c3=self.ax.figure.canvas.mpl_connect('motion_notify_event', self.onmove)

    def onclick(self,event):
        if event.inaxes == self.ax:
            if event.button == self.button:
                self.func(event, self.ax)
    def onpress(self,event):
        self.press=True
    def onmove(self,event):
        if self.press:
            self.move=True
    def onrelease(self,event):
        if self.press and not self.move:
            self.onclick(event)
        self.press=False; self.move=False


def func(event, ax):
    print(event.xdata, event.ydata)
    ax.scatter(event.xdata, event.ydata,marker='*',color='yellow')
    ax.figure.canvas.draw()

path = 'figuras/Pereira/'
list_image = listdir(path)
file = path + list_image[17]

print(file)

image = mpimg.imread(file)

fig, (ax2) = plt.subplots(1)

imgplot = ax2.imshow(image)
fig.canvas.draw()
plt.draw()
click = Click(ax2, func, button=1)
plt.show()