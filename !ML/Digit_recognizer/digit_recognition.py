from tkinter import *
from tkinter import ttk,colorchooser,filedialog
import PIL
from PIL import ImageGrab
from model_predict import predict

class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = '#000000'
        self.color_bg = '#ffffff'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)
        self.c.bind('<ButtonRelease-1>',self.reset)

    def paint(self,e):
        if(self.old_x and self.old_y):
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)

        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):
        self.old_x = None
        self.old_y = None

    def changeW(self,e):
        self.penwidth = e

    def save(self):
        x = self.master.winfo_rootx() + self.c.winfo_x()
        y = self.master.winfo_rooty() + self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        image = PIL.ImageGrab.grab().crop((x,y,x1,y1)).save("image/test.png")

    def put_text(self):
        data = predict("image/test.png")
        for digit in data:
            k,m,n = digit
            self.c.create_text(k,m,text=n,fill="red",font="Times 40 italic bold",anchor="center")

    def clear(self):
        self.c.delete(ALL)

    def change_bg(self):
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg

    def drawWidgets(self):
        self.controls = Frame(self.master,padx=5,pady=5)
        Label(self.controls,text='Pen Width: ',font=('',15)).grid(row=0,column=0)
        self.slider = ttk.Scale(self.controls,from_=5,to=100,command=self.changeW,orient=HORIZONTAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=0,column=1,ipadx=30)
        self.controls.pack()

        self.c = Canvas(self.master,width=800,height=500,bg=self.color_bg,)
        self.c.pack(fill=BOTH,expand=True)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        filename=Menu(menu)
        menu.add_cascade(label='File..',menu=filename)
        filename.add_command(label='Export..',command=self.save)
        colormenu= Menu(menu)
        menu.add_cascade(label='Colors',menu=colormenu)
        colormenu.add_command(label='Brush Color',command=self.change_bg)
        colormenu.add_command(label='Background Color', command=self.change_bg)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Options', menu=optionmenu)
        optionmenu.add_command(label='Recognite Object',command=self.put_text)
        optionmenu.add_command(label='Clear Canvas', command=self.clear)
        optionmenu.add_command(label='Exit', command=self.master.destroy)


if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('digit recognition')
    root.mainloop()





