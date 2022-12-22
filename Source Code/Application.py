"""
**********************************************
**********************************************
**********         MuCAD V3         **********
**********   By: Mustapha Ossama    **********
**********     Date: 7/2/2022      **********
**********************************************
**********************************************
**********************************************
"""





from tkinter import*
from tkinter import messagebox
from turtle import*
from PIL import Image, ImageTk
import math 
import time
import numpy as np

"""
###############################
######                  #######
######  Manual Drawing  #######
######                  #######
###############################
"""

def drawpixel(x, y,Object, pixelsize = 1 ):
    Object.penup()
    Object.setpos(x*pixelsize,y*pixelsize)
    Object.pendown()
    Object.forward(pixelsize)


def drawLine(x1,y1,x2,y2,OBJ):
    #determine start point
    if x1>x2:
        start = [x2,y2]
    else:
        start = [x1,y1]
        
    #get delta x and delta y
    deltax = abs(x1-x2)
    deltay = abs(y1-y2)
    
    #get number of steps
    if(deltax>deltay):
        steps = deltax
    
    else:
        steps = deltay
        
    #get the increment
    xinc = float(deltax/steps)
    yinc = float(deltay/steps)

    #draw the line
    for i in range(steps):
        drawpixel(int(start[0]),int(start[1]),OBJ)
        start[0] += xinc
        if y1<y2:
            start[1] += yinc
        else:
            start[1] -= yinc





"""
*******************************
******   Main window    *******
*******************************
"""


#window creation
window = Tk()
#set title name
window.title("Mu CAD") 
#set icon picture
window.iconbitmap("icon.ico")
#set window size
window.geometry("1400x800")
#fix window size
#window.resizable(False, False)
#set window backround
window.configure(background='light gray')








   
   
"""
*******************************
******   Choose Mode    *******
*******************************
"""

def ChoosePlaneFunction():
    global ChoosePlaneVar
    ChoosePlaneVar = ChoosePlaneVariable.get()
    Choose()    

   
ChoosePlaneVariable = StringVar()
ChoosePlaneVar = "NAN"
OnePlaneButton = Radiobutton(window,width=20,height=5, text= "Draw on One Plane",font = 10,variable = ChoosePlaneVariable, value = "One Plane", command= lambda:ChoosePlaneFunction())
ThreePlaneButton = Radiobutton(window,width=20,height=5,  text= "Draw on Three Planes",font = 10,variable = ChoosePlaneVariable, value = "Three Planes", command= lambda:ChoosePlaneFunction())

OnePlaneButton.place(x=500,y=300)
ThreePlaneButton.place(x=500,y=500)





IMG = ImageTk.PhotoImage(Image.open("MuCAD.png"))
IMGLabel = Label(window, image=IMG)
IMGLabel.place(x=500,y=0)





EntitiesCanvasIndex = 0.0
Entities = []
buffer = []
def Choose():


    global GcodeLines
    global GcodeCanvasIndex

    GcodeLines = []
    GcodeCanvasIndex = 0.0
    
    """
    ###############################
    ######                  #######
    ######    Three Views   #######
    ######    Elevation     #######
    ######    Side          #######
    ######    Top           #######
    ######                  #######
    ###############################

    """        
        
        
    if ChoosePlaneVar == "Three Planes":
        """
        *******************************
        ******     Canvases     *******
        *******************************
        """
        OnePlaneButton.destroy()
        ThreePlaneButton.destroy()

        #Definitions
        CanvasSizeX = 250
        CanvasSizeY = 250
        SideOffsetX = 100
        TopOffsetY = 100


        ElevationShiftX = 50
        ElevationShiftY = 150

        SideShiftX = SideOffsetX + ElevationShiftX + CanvasSizeX
        SideShiftY = ElevationShiftY

        TopShiftX = ElevationShiftX
        TopShiftY = TopOffsetY + ElevationShiftY + CanvasSizeY




        #Elevation view region (canvas)
        ElevationCanvas = Canvas(window, height=CanvasSizeX, width=CanvasSizeY )
        ElevationCanvas.place(x = ElevationShiftX, y = ElevationShiftY)

        #Top view region (canvas)
        TopCanvas = Canvas(window, height=CanvasSizeX, width=CanvasSizeY )
        TopCanvas.place(x = SideShiftX, y = SideShiftY)

        #Side view region (canvas)
        SideCanvas = Canvas(window, height=CanvasSizeX, width=CanvasSizeY)
        SideCanvas.place(x = TopShiftX, y = TopShiftY)



        #Log (canvas)
        GcodeCanvasWidth = 400
        GcodeCanvasHeight = 800


        GcodeCanvas = Text(window, height=GcodeCanvasHeight, width=GcodeCanvasWidth)
        GcodeCanvas.place(x=1000,y=50)

        ElevationScreen = TurtleScreen(ElevationCanvas)
        SideScreen = TurtleScreen(SideCanvas)
        TopScreen = TurtleScreen(TopCanvas)


        ElevationTurtle = RawTurtle(ElevationScreen)
        SideTurtle = RawTurtle(SideScreen)
        TopTurtle = RawTurtle(TopScreen)



        ElevationTurtle.hideturtle()
        SideTurtle.hideturtle()
        TopTurtle.hideturtle()









        """
        *******************************
        ******       Text       *******
        *******************************
        """

        #Titles 

        #Elevation Top Side Titles
        ElevationText = Label(window,text = "Elevation", fg = "black",font = 5,bg = "light green", height = 1, width = 10)
        TopText = Label(window,text = "Top", fg = "black",font = 5,bg = "light green", height = 1, width = 10)
        SideText = Label(window,text = "Side", fg = "black",font = 5,bg = "light green", height = 1, width = 10)

        TextOffsetY = 10

        ElevationText.place(x=TopShiftX+(CanvasSizeX*0.5)-55, y=SideShiftY+CanvasSizeY+TextOffsetY)
        SideText.place(x=TopShiftX+(CanvasSizeX*0.5)-55, y=TopShiftY+CanvasSizeY+TextOffsetY)
        TopText.place(x=SideShiftX+(CanvasSizeX*0.5)-55, y=SideShiftY+CanvasSizeY+TextOffsetY)


        #Gcode Titles
        GcodeText = Label(window,text = "G Code LOG", fg = "black",font = 5,bg = "light green", height = 2, width = 50)
        GcodeText.place(x=1000, y=0)



        #Tiltes (Entries)

        X1Text = Label(window, text="X1",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        Y1Text = Label(window, text="Y1",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        X2Text = Label(window, text="X2",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        Y2Text = Label(window, text="Y2",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        LengthText = Label(window, text="Length",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        RediusText = Label(window, text="Redius",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        AngleText = Label(window, text="Angle",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        SidesText = Label(window, text="Sides",fg="black", bg = "light blue",font = 5, height = 1, width = 10)

        EntryOffsetX = 80
        EntryOffsetY = 50


        X1Text.place(x=SideShiftX+CanvasSizeX+EntryOffsetX, y=TopOffsetY+(EntryOffsetY*1)+2)
        Y1Text.place(x=SideShiftX+CanvasSizeX+EntryOffsetX, y=TopOffsetY+(EntryOffsetY*2))
        X2Text.place(x=SideShiftX+CanvasSizeX+EntryOffsetX, y=TopOffsetY+(EntryOffsetY*3))
        Y2Text.place(x=SideShiftX+CanvasSizeX+EntryOffsetX, y=TopOffsetY+(EntryOffsetY*4))
        LengthText.place(x=SideShiftX+CanvasSizeX+EntryOffsetX, y=TopOffsetY+(EntryOffsetY*5))
        RediusText.place(x=SideShiftX+CanvasSizeX+EntryOffsetX, y=TopOffsetY+(EntryOffsetY*6))
        AngleText.place(x=SideShiftX+CanvasSizeX+EntryOffsetX, y=TopOffsetY+(EntryOffsetY*7))
        SidesText.place(x=SideShiftX+CanvasSizeX+EntryOffsetX, y=TopOffsetY+(EntryOffsetY*8))


        #Plane to draw (Elevation, Side, Top)
        PlaneText = Label(window, text="Plane Select",fg="black",font='sans 9 bold', bg = "mediumpurple", height = 3, width = 35)
        PlaneText.place(x=750,y=0)









        """
        *******************************
        ******     Entries      *******
        *******************************
        """
        X1Input = Entry(window, font=5, fg="black", bg="white",width=8)
        Y1Input = Entry(window, font=5, fg="black", bg="white",width=8)
        X2Input = Entry(window, font=5, fg="black", bg="white",width=8)
        Y2Input = Entry(window, font=5, fg="black", bg="white",width=8)
        LengthInput = Entry(window, font=5, fg="black", bg="white",width=8)
        RediusInput = Entry(window, font=5, fg="black", bg="white",width=8)
        AngleInput = Entry(window, font=5, fg="black", bg="white",width=8)
        SidesInput = Entry(window, font=5, fg="black", bg="white",width=8)



        SeperationX = 130
        SeperationY = 50

        X1OffsetX = SideShiftX+CanvasSizeX+EntryOffsetX + SeperationX
        X1OffsetY = TopOffsetY+(EntryOffsetY*1)-49



        X1Input.place(x=X1OffsetX, y=X1OffsetY + (SeperationY*1))
        Y1Input.place(x=X1OffsetX, y=X1OffsetY + (SeperationY*2))
        X2Input.place(x=X1OffsetX, y=X1OffsetY + (SeperationY*3))
        Y2Input.place(x=X1OffsetX, y=X1OffsetY + (SeperationY*4))
        LengthInput.place(x=X1OffsetX, y=X1OffsetY + (SeperationY*5))
        RediusInput.place(x=X1OffsetX, y=X1OffsetY + (SeperationY*6))
        AngleInput.place(x=X1OffsetX, y=X1OffsetY + (SeperationY*7))
        SidesInput.place(x=X1OffsetX, y=X1OffsetY + (SeperationY*8))










        """
        *******************************
        ******    Title Bar     *******
        *******************************
        """
        #add menu
        myMenu = Menu(window)
        window.config(menu = myMenu)

        #add file menu
        def NewFileFunc():
            #Clear Planes
            ClearAllEditFunc()
            #Clear Inputs
            X1Input.delete(0,END)
            Y1Input.delete(0,END)
            X2Input.delete(0,END)
            Y2Input.delete(0,END)
            LengthInput.delete(0,END)
            RediusInput.delete(0,END)
            AngleInput.delete(0,END)
            SidesInput.delete(0,END)

            
            
        def ExitFileFunc():
            window.quit()
            
        FileMenu = Menu(myMenu)
        myMenu.add_cascade(label="file", menu = FileMenu)
        FileMenu.add_command(label="New", command= lambda:NewFileFunc())
        FileMenu.add_separator()
        FileMenu.add_command(label="Exit", command= lambda:ExitFileFunc())



        #add edit menu
        def UndoEditFunc():
            if(PlaneSelect != "Side" and PlaneSelect != "Top" ):
                ElevationTurtle.undo()
                
                #for G Code

                GcodeLines.pop()

                GcodeCanvas.delete(0.0,END)
                
                for i in range(0,len(GcodeLines)-1):
                    GcodeCanvas.insert(float(i),GcodeLines[int(i)])
                
                
            elif(PlaneSelect == "Side"):
                SideTurtle.undo()

                  
                
            elif(PlaneSelect == "Top"):
                TopTurtle.undo()



        def ClearAllEditFunc():
            ElevationTurtle.penup()
            SideTurtle.penup()
            TopTurtle.penup()
            ElevationTurtle.clear()
            ElevationTurtle.home()
            SideTurtle.clear()
            SideTurtle.home()
            TopTurtle.clear()
            TopTurtle.home()
                 

            
            
        EditMenu = Menu(myMenu)
        myMenu.add_cascade(label="edit", menu = EditMenu)
        EditMenu.add_command(label="Undo", command= lambda:UndoEditFunc())
        EditMenu.add_separator()
        EditMenu.add_command(label="ClearALL", command= lambda:ClearAllEditFunc())




        #Help file menu
        def CartesianLineHelpFunc():
            messagebox.showinfo("Cartesian Line","Select Plane\nFill X1\nFill Y1\nFill X2\nFill Y2")
            
            
        def PolarLineHelpFunc():
            messagebox.showinfo("Polar Line","Select Plane\nFill X1\nFill Y1\nFill Angle\nFill Redius")

            
        def ArcHelpFunc():
            messagebox.showinfo("Arc/Circles","Select Plane\nFill X1\nFill Y1\nFill Redius\nFill Angle")

            
        def RectangleHelpFunc():
            messagebox.showinfo("Rectangle","Select Plane\nFill X1\nFill Y1\nFill X2\nFill Y2")
          
          
        def PolygonHelpFunc():
            messagebox.showinfo("Polygon","Select Plane\nFill X1\nFill Y1\nFill Redius\nFill Sides ")

            
        HelpMenu = Menu(myMenu)
        myMenu.add_cascade(label="Help", menu = HelpMenu)
        HelpMenu.add_command(label="How to draw a Cartesian line", command= lambda:CartesianLineHelpFunc())
        HelpMenu.add_separator()
        HelpMenu.add_command(label="How to draw a Polar line", command= lambda:PolarLineHelpFunc())
        HelpMenu.add_separator()
        HelpMenu.add_command(label="How to draw an Arc", command= lambda:ArcHelpFunc())
        HelpMenu.add_separator()
        HelpMenu.add_command(label="How to draw a Rectangle", command= lambda:RectangleHelpFunc())
        HelpMenu.add_separator()
        HelpMenu.add_command(label="How to draw a Polygon", command= lambda:PolygonHelpFunc())












        """
        *******************************
        ******    Gadget Bar    *******
        *******************************
        """
        #optionMenu functions
        def clearEntries():
            #Clear Inputs
            X1Input.delete(0,END)
            Y1Input.delete(0,END)
            X2Input.delete(0,END)
            Y2Input.delete(0,END)
            LengthInput.delete(0,END)
            RediusInput.delete(0,END)
            AngleInput.delete(0,END)
            SidesInput.delete(0,END)
            

        #Plane Select  (Elevation, Side, Top)
        def PlaneSelectFunction():
            global PlaneSelect
            PlaneSelect = "Elevation"
            PlaneSelect = PlaneVariable.get()
            


        #CartesianLine function
        def CartesianLineFunction():

            #get user inputs
            x1 = float(X1Input.get())-(CanvasSizeX/2)
            y1 = float(Y1Input.get())-(CanvasSizeY/2)
            x2 = float(X2Input.get())-(CanvasSizeX/2)
            y2 = float(Y2Input.get())-(CanvasSizeY/2)
            
            clearEntries()

            if(PlaneSelect == "Elevation" ):
                #set starting position to write the line
                ElevationTurtle.penup()
                ElevationTurtle.setx(int(x1))
                ElevationTurtle.sety(int(y1))

               
                #drawing
                ElevationTurtle.pendown()
                ElevationTurtle.goto(int(x2),int(y2))
                
                global GcodeCanvasIndex
                #for G CODE
                GcodeLines.append("G01 X{} Y{}\n".format(x2+(CanvasSizeX/2),y2+(CanvasSizeX/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                
            elif(PlaneSelect == "Side"):
                #set starting position to write the line
                SideTurtle.penup()
                SideTurtle.setx(int(x1))
                SideTurtle.sety(int(y1))

               
                #drawing
                SideTurtle.pendown()
                SideTurtle.goto(int(x2),int(y2))
                    
                
            elif(PlaneSelect == "Top"):
                #set starting position to write the line
                TopTurtle.penup()
                TopTurtle.setx(int(x1))
                TopTurtle.sety(int(y1))

               
                #drawing
                TopTurtle.pendown()
                TopTurtle.goto(int(x2),int(y2))

            
            
            
        #RAngleLine function
        def RCitaLineFunction():

            #get user inputs
            x1 = float(X1Input.get())-(CanvasSizeX/2)
            y1 = float(Y1Input.get())-(CanvasSizeY/2)
            R = float(RediusInput.get())
            Angle = float(AngleInput.get()) #Angle is Cita
            
            x2 = R*(math.cos(math.radians(Angle)))+x1
            y2 = R*(math.sin(math.radians(Angle)))+y1
            
            clearEntries()
            if(PlaneSelect != "Side" and PlaneSelect != "Top" ):
                #set starting position to write the line
                ElevationTurtle.penup()
                ElevationTurtle.home()
                ElevationTurtle.setx(int(x1))
                ElevationTurtle.sety(int(y1))

               
                #drawing
                ElevationTurtle.pendown()
                ElevationTurtle.goto(int(x2),int(y2))
         
         
                #for G CODE
                global GcodeCanvasIndex
                GcodeLines.append("G01 X{} Y{}\n".format(round(x2+(CanvasSizeX/2),3),round(y2+(CanvasSizeX/2),3)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                
            elif(PlaneSelect == "Side"):
                #set starting position to write the line
                SideTurtle.penup()
                SideTurtle.home()
                SideTurtle.setx(int(x1))
                SideTurtle.sety(int(y1))

               
                #drawing
                SideTurtle.pendown()
                SideTurtle.goto(int(x2),int(y2))
                
                
                
            elif(PlaneSelect == "Top"):
                #set starting position to write the line
                TopTurtle.penup()
                SideTurtle.home()
                TopTurtle.setx(int(x1))
                TopTurtle.sety(int(y1))

               
                #drawing
                TopTurtle.pendown()
                TopTurtle.goto(int(x2),int(y2))
         
         
         
        #ArcCircle function
        def ArcCircleFunction():

            #get user inputs
            x1 = float(X1Input.get())-(CanvasSizeX/2)
            y1 = float(Y1Input.get())-(CanvasSizeY/2)
            R = float(RediusInput.get())
            Angle = float(AngleInput.get()) #Angle is Cita
            
            clearEntries()


            if(PlaneSelect != "Side" and PlaneSelect != "Top" ):
                #set starting position to write the line
                ElevationTurtle.penup()
                ElevationTurtle.home()
                ElevationTurtle.setx(int(x1))
                ElevationTurtle.sety(int(y1))
               
                #drawing
                ElevationTurtle.pendown()
                ElevationTurtle.circle(R,Angle)

         
                #for G CODE        
                I,J = ElevationTurtle.pos()        
                global GcodeCanvasIndex
                if Angle < 0:
                    GcodeLines.append("G02 X{} Y{} I{} J{}\n".format(x1+(CanvasSizeX/2),y1+(CanvasSizeX/2),round(I+(CanvasSizeX/2),3),round(J+(CanvasSizeX/2)),3))
                
                elif Angle >= 0:
                    GcodeLines.append("G03 X{} Y{} I{} J{}\n".format(x1+(CanvasSizeX/2),y1+(CanvasSizeX/2),round(I+(CanvasSizeX/2),3),round(J+(CanvasSizeX/2)),3))

                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                
                
            elif(PlaneSelect == "Side"):
                #set starting position to write the line
                SideTurtle.penup()
                SideTurtle.home()
                SideTurtle.setx(int(x1))
                SideTurtle.sety(int(y1))
               
                #drawing
                SideTurtle.pendown()
                SideTurtle.circle(R,Angle)

                    
            elif(PlaneSelect == "Top"):
                #set starting position to write the line
                TopTurtle.penup()
                TopTurtle.home()
                TopTurtle.setx(int(x1))
                TopTurtle.sety(int(y1))
               
                #drawing
                TopTurtle.pendown()
                TopTurtle.circle(R,Angle)

                    

                    
        #ArcCircle function
        def RectangleFunction():

            #get user inputs
            x1 = float(X1Input.get())-(CanvasSizeX/2)
            y1 = float(Y1Input.get())-(CanvasSizeY/2)
            x2 = float(X2Input.get())-(CanvasSizeX/2)
            y2 = float(Y2Input.get())-(CanvasSizeY/2)
            
            clearEntries()


            if(PlaneSelect != "Side" and PlaneSelect != "Top" ):
                #set starting position to write the line
                ElevationTurtle.penup()
                ElevationTurtle.home()
                ElevationTurtle.setx(int(x1))
                ElevationTurtle.sety(int(y1))
               
               
               
                #drawing first line
                ElevationTurtle.pendown()
                ElevationTurtle.goto(x2,y1)
                M,N = ElevationTurtle.pos()

                #for G CODE
                global GcodeCanvasIndex
                GcodeLines.append("G01 X{} Y{}\n".format(M+(CanvasSizeX/2),N+(CanvasSizeX/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                
                       
                #drawing second line
                ElevationTurtle.pendown()
                ElevationTurtle.goto(x2,y2)
                M,N = ElevationTurtle.pos()

                #for G CODE
                GcodeLines.append("G01 X{} Y{}\n".format(M+(CanvasSizeX/2),N+(CanvasSizeX/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                
                #drawing third line
                ElevationTurtle.pendown()
                ElevationTurtle.goto(x1,y2)
                M,N = ElevationTurtle.pos()

                #for G CODE
                GcodeLines.append("G01 X{} Y{}\n".format(M+(CanvasSizeX/2),N+(CanvasSizeX/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                #drawing fourth line
                ElevationTurtle.pendown()
                ElevationTurtle.goto(x1,y1)
                M,N = ElevationTurtle.pos()
                #for G CODE
                GcodeLines.append("G01 X{} Y{}\n".format(M+(CanvasSizeX/2),N+(CanvasSizeX/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
         
            elif(PlaneSelect == "Side"):
                #set starting position to write the line
                SideTurtle.penup()
                SideTurtle.home()
                SideTurtle.setx(int(x1))
                SideTurtle.sety(int(y1))
               
                #drawing first line
                SideTurtle.pendown()
                SideTurtle.goto(x2,y1)
                       
                #drawing second line
                SideTurtle.pendown()
                SideTurtle.goto(x2,y2)
                
                #drawing third line
                SideTurtle.pendown()
                SideTurtle.goto(x1,y2)
                
                #drawing second line
                SideTurtle.pendown()
                SideTurtle.goto(x1,y1)
             
            elif(PlaneSelect == "Top"):
                #set starting position to write the line
                TopTurtle.penup()
                TopTurtle.home()
                TopTurtle.setx(int(x1))
                TopTurtle.sety(int(y1))
               
                #drawing first line
                TopTurtle.pendown()
                TopTurtle.goto(x2,y1)
                       
                #drawing second line
                TopTurtle.pendown()
                TopTurtle.goto(x2,y2)
                
                #drawing third line
                TopTurtle.pendown()
                TopTurtle.goto(x1,y2)
                
                #drawing fourth line
                TopTurtle.pendown()
                TopTurtle.goto(x1,y1)
         
         
        def PolygonFunction():

            #get user inputs
            x1 = float(X1Input.get())-(CanvasSizeX/2)
            y1 = float(Y1Input.get())-(CanvasSizeY/2)
            R = float(RediusInput.get())
            Sides = int(SidesInput.get())
            
            clearEntries()


            if(PlaneSelect != "Side" and PlaneSelect != "Top" ):
                #set starting position to write the line
                ElevationTurtle.penup()
                ElevationTurtle.home()
                ElevationTurtle.setx(int(x1))
                ElevationTurtle.sety(int(y1))
               
                #drawing
                ElevationTurtle.pendown()
                ElevationTurtle.circle(R, steps = Sides)
             
             

             
            elif(PlaneSelect == "Side"):
                #set starting position to write the line
                SideTurtle.penup()
                SideTurtle.home()
                SideTurtle.setx(int(x1))
                SideTurtle.sety(int(y1))
               
                #drawing
                SideTurtle.pendown()
                SideTurtle.circle(R, steps = Sides)
             
         

                    
            elif(PlaneSelect == "Top"):
                #set starting position to write the line
                TopTurtle.penup()
                TopTurtle.home()
                TopTurtle.setx(int(x1))
                TopTurtle.sety(int(y1))
               
                #drawing
                TopTurtle.pendown()
                TopTurtle.circle(R, steps = Sides)
             
             
                        
             
        def ClearFunction() :

            if(PlaneSelect != "Side" and PlaneSelect != "Top" ):
                ElevationTurtle.penup()
                ElevationTurtle.clear()
                ElevationTurtle.home()
                 
                 

             
            elif(PlaneSelect == "Side"):
                SideTurtle.penup()
                SideTurtle.clear()
                SideTurtle.home()

                    
            elif(PlaneSelect == "Top"):
                TopTurtle.penup()
                TopTurtle.clear()
                TopTurtle.home()
                 

         
         
        #optionMenu Drawings

        #cartesian line (needs x1, y1, x2, y2)
        CartLine = Button(window,text="Cartesian Line",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = CartesianLineFunction)
        CartLine.place(x=0,y=0)


        #Redius and Cita line (needs x1, y1, Reduis, Angle)
        RCitaLine = Button(window,text="R/Angle Line",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = RCitaLineFunction)
        RCitaLine.place(x=100,y=0)


        #Arc Circles (needs x1, y1, Reduis, Angle)
        ArcCircle = Button(window,text="Arc",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = ArcCircleFunction)
        ArcCircle.place(x=200,y=0)


        #Rectangle Circles (needs x1, y1, x2, y2)
        Rectangle = Button(window,text="Rectangle",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = RectangleFunction)
        Rectangle.place(x=300,y=0)


        #Polygon (needs x1, y1, R, Num)
        Polygon = Button(window,text="Polygon",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = PolygonFunction)
        Polygon.place(x=400,y=0)


        #Clear
        Clear = Button(window,text="Clear",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = ClearFunction)
        Clear.place(x=0,y=45)


        #Plane to draw
        PlaneVariable = StringVar()

        ElevationPlaneButton = Radiobutton(window,width=9,height=2, text= "Elevation",variable = PlaneVariable, value = "Elevation",command = lambda: PlaneSelectFunction())
        SidePlaneButton = Radiobutton(window,width=9,height=2,  text= "Side",variable = PlaneVariable, value = "Side",command = lambda: PlaneSelectFunction())
        TopPlaneButton = Radiobutton(window,width=9,height=2,  text= "Top",variable = PlaneVariable, value = "Top",command = lambda: PlaneSelectFunction())

        ElevationPlaneButton.place(x=750, y=55)
        SidePlaneButton.place(x=835, y=55)
        TopPlaneButton.place(x=909, y=55)
        
        
        
        
        
        
        
        
        
        
        
        
        
    """
    ###############################
    ######                  #######
    ######     One View     #######
    ######                  #######
    ###############################
    """        
        
        
       
        
        
    if ChoosePlaneVar == "One Plane":
        """
        *******************************
        ******     Canvases     *******
        *******************************
        """
        
        OnePlaneButton.destroy()
        ThreePlaneButton.destroy()
        #Definitions
        Entities = []  
                            #Line -> x1, y1, x2, y2
                            #rectangle -> x1, y1, x2, y2
                            #Arc  -> x1, y1, startAngle, endAngle, Redius
        
        CanvasSizeX = 800
        CanvasSizeY = 600
        SideOffsetX = 100
        TopOffsetY = 100


        ElevationShiftX = 50
        ElevationShiftY = 150

        SideShiftX = SideOffsetX + ElevationShiftX + CanvasSizeX
        SideShiftY = ElevationShiftY

        TopShiftX = ElevationShiftX
        TopShiftY = TopOffsetY + ElevationShiftY + CanvasSizeY



        #Elevation view region (canvas)
        ElevationCanvas = Canvas(window, height=CanvasSizeY, width=CanvasSizeX )
        ElevationCanvas.place(x = ElevationShiftX, y = ElevationShiftY)




        #Log (canvas)
        GcodeCanvasWidth = 200
        GcodeCanvasHeight = 800

        GcodeLines = []
        
        


        
        #Gcode Canvas
        GcodeCanvas = Text(window, height=GcodeCanvasHeight, width=GcodeCanvasWidth)
        GcodeCanvas.place(x=1200,y=50)
        GcodeCanvasIndex = 0.0

        ElevationScreen = TurtleScreen(ElevationCanvas)



        ElevationTurtle = RawTurtle(ElevationScreen)


        """
        *******************************
        ******  Initialization  *******
        *******************************
        """     
        ElevationTurtle.hideturtle()
        ElevationTurtle.setundobuffer(100)
        ElevationTurtle.speed(10)










        """
        *******************************
        ******       Text       *******
        *******************************
        """

        
        
        
        
        #Titles 
        TextOffsetY = 10



        #Gcode Titles
        GcodeText = Label(window,text = "G Code LOG", fg = "black",font = 5,bg = "light green", height = 2, width = 30)
        GcodeText.place(x=1200, y=0)


      

        #Tiltes (Entries)
        DXFFileName = Label(window, text="DXF File Name",fg="black", bg = "light blue",font = 5, height = 1, width = 15)
        GcodeFileName = Label(window, text="Gcode File Name",fg="black", bg = "light blue",font = 5, height = 1, width = 15)
        ValueAEntryText = Label(window, text="Value A",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        ValueBEntryText = Label(window, text="Value B",fg="black", bg = "light blue",font = 5, height = 1, width = 10)
        SelectedEntitiyEntryText = Label(window, text="Selected Entites",fg="black", bg = "light blue",font = 5, height = 1, width = 15)      
        

        EntryOffsetX = 80
        EntryOffsetY = 50


        DXFFileName.place(x=CanvasSizeX+EntryOffsetX-130, y=0)
        GcodeFileName.place(x=CanvasSizeX+EntryOffsetX-130, y=50)
        ValueAEntryText.place(x=230, y=90)
        ValueBEntryText.place(x=380, y=90)
        SelectedEntitiyEntryText.place(x=0, y=90)
        









        """
        *******************************
        ******     Entries      *******
        *******************************
        """
        DXFEntry = Entry(window, font=5, fg="black", bg="white",width=25)
        GcodeEntry = Entry(window, font=5, fg="black", bg="white",width=25)
        ValueAEntry = Entry(window, font=5, fg="black", bg="white",width=10)
        ValueBEntry = Entry(window, font=5, fg="black", bg="white",width=10)
        SelectedEntitiesEntry = Entry(window, font=5, fg="black", bg="white",width=15)


        SeperationX = 130
        SeperationY = 50

        X1OffsetX = 1000
        X1OffsetY = TopOffsetY+(EntryOffsetY*1)-49



        DXFEntry.place(x=X1OffsetX-80, y=0)
        GcodeEntry.place(x=X1OffsetX-80, y=50)

        ValueAEntry.place(x=230, y=120)
        ValueBEntry.place(x=380, y=120)
        SelectedEntitiesEntry.place(x=0, y=120)






        """
        *******************************
        ******    Title Bar     *******
        *******************************
        """
        #add menu
        myMenu = Menu(window)
        window.config(menu = myMenu)

        #add file menu
        def NewFileFunc():
            #Clear Planes
            ClearAllEditFunc()
            #Clear Inputs
            buffer = []
            Entities = []

            
            
        def ExitFileFunc():
            window.quit()
            
            
        def ExportDXF():
            global Entities
            sortedEntities = Entities
            for i in range(len(sortedEntities)-1):
                for j in range(len(sortedEntities)-i-1):
                    if(sortedEntities[j][0] == "circle"):
                        sac = sortedEntities[j]
                        sortedEntities[j] = sortedEntities[j+1]
                        sortedEntities[j+1] = sac
            filepath = DXFEntry.get()
            if filepath == "":
                messagebox.showinfo("DXF File Name is Emptty","Fill DXF File Name")


            
            dxffile = open(filepath,'a+')
            dxffile.close()
            dxffile = open(filepath,'w')
            dxffile.close()

            dxffile = open(filepath,'a+')
            #write the start sections
            startSection = open('Start.txt','r')
            lines = startSection.readlines()
            startSection.close()
            for line in lines:
                dxffile.write(line)
                
            #write the Entity Sections 
            entitylist = []            
            linefile = open('Line.txt','r')
            linelines = linefile.readlines()
            linefile.close()
            circlefile = open('Circle.txt','r')
            circlelines = circlefile.readlines()
            circlefile.close()
            
            for entity in sortedEntities:
                #detect line
                if entity[0] == 'line':
                    for i in range(len(linelines)):
                        if linelines[i].strip() == "10" and linelines[i][0] == " ":
                            entitylist.append(linelines[i])
                            entitylist.append(str(entity[1])+'\n')
                        elif linelines[i].strip() == "20"  and linelines[i][0] == " ":
                            entitylist.append(linelines[i])
                            entitylist.append(str(entity[2])+'\n')
                        elif linelines[i].strip() == "11"  and linelines[i][0] == " ":
                            entitylist.append(linelines[i])
                            entitylist.append(str(entity[3])+'\n')
                        elif linelines[i].strip() == "21"  and linelines[i][0] == " ":
                            entitylist.append(linelines[i])
                            entitylist.append(str(entity[4])+'\n')
                        else:
                            entitylist.append(linelines[i])


                #detect circle
                elif entity[0] == 'circle':
                    for i in range(len(circlelines)):
                        if circlelines[i].strip() == "10" and circlelines[i][0] == " ":
                            entitylist.append(circlelines[i])
                            entitylist.append(str(entity[1])+'\n')

                        elif circlelines[i].strip() == "20"  and circlelines[i][0] == " ":
                            entitylist.append(circlelines[i])
                            entitylist.append(str(entity[2])+'\n')
                        
                        elif circlelines[i].strip() == "40"  and circlelines[i][0] == " ":
                            entitylist.append(circlelines[i])
                            entitylist.append(str(entity[3])+'\n')

                        else:
                            entitylist.append(circlelines[i])     
            for j in entitylist:
                dxffile.write(j)
            
            #write the end sections
            endSection = open('End.txt','r')
            lines = endSection.readlines()
            endSection.close()
            for line in lines:
                dxffile.write(line)
            
        def ExportGcode():
            global GcodeLines
            filepath = GcodeEntry.get()
            if filepath == "":
                messagebox.showinfo("GCODE File Name is Emptty","Fill GCODE File Name")
            
            
            Gcodefile = open(filepath,'a+')
            Gcodefile.close()
            Gcodefile = open(filepath,'w')
            Gcodefile.close()
            Gcodefile = open(filepath,'a+')
            for i in GcodeLines:
                Gcodefile.write(i)
                    
                
            
        FileMenu = Menu(myMenu)
        myMenu.add_cascade(label="file", menu = FileMenu)
        FileMenu.add_command(label="New", command= lambda:NewFileFunc())
        FileMenu.add_separator()
        FileMenu.add_command(label="Export DXF", command= lambda:ExportDXF())
        FileMenu.add_separator()
        FileMenu.add_command(label="Export Gcode", command= lambda:ExportGcode())
        FileMenu.add_separator()
        FileMenu.add_command(label="Exit", command= lambda:ExitFileFunc())



        #add edit menu
        def UndoEditFunc():
            ElevationTurtle.undo()
            
            #for G Code

            GcodeLines.pop()

            GcodeCanvas.delete(0.0,END)
            
            for i in range(0,len(GcodeLines)-1):
                GcodeCanvas.insert(float(i),GcodeLines[int(i)])
                
       



        def ClearAllEditFunc():
            ElevationTurtle.penup()
            ElevationTurtle.clear()
            ElevationTurtle.home()

            
            
        EditMenu = Menu(myMenu)
        myMenu.add_cascade(label="edit", menu = EditMenu)
        EditMenu.add_command(label="Undo", command= lambda:UndoEditFunc())
        EditMenu.add_separator()
        EditMenu.add_command(label="ClearALL", command= lambda:ClearAllEditFunc())




        #Help file menu
        def CartesianLineHelpFunc():
            messagebox.showinfo("Cartesian Line","Select Plane\nFill X1\nFill Y1\nFill X2\nFill Y2")
            
            
        def CircleHelpFunc():
            messagebox.showinfo("Circle","Select Plane\nFill X1\nFill Y1\nFill Angle\nFill Redius")

            
        def ArcHelpFunc():
            messagebox.showinfo("Arc/Circles","Select Plane\nFill X1\nFill Y1\nFill Redius\nFill Angle")

            
        def RectangleHelpFunc():
            messagebox.showinfo("Rectangle","Select Plane\nFill X1\nFill Y1\nFill X2\nFill Y2")
          
          
            
        HelpMenu = Menu(myMenu)
        myMenu.add_cascade(label="Help", menu = HelpMenu)
        HelpMenu.add_command(label="How to draw a Cartesian line", command= lambda:CartesianLineHelpFunc())
        HelpMenu.add_separator()
        HelpMenu.add_command(label="How to draw a Circle", command= lambda:CircleHelpFunc())
        HelpMenu.add_separator()
        HelpMenu.add_command(label="How to draw an Arc", command= lambda:ArcHelpFunc())
        HelpMenu.add_separator()
        HelpMenu.add_command(label="How to draw a Rectangle", command= lambda:RectangleHelpFunc())
        HelpMenu.add_separator()












        """
        *******************************
        ******    Gadget Bar    *******
        *******************************
        """
        #optionMenu functions
    

        def GetPos(x,y):
            global buffer
            buffer.append([x,y])
            print("#########")
            print(buffer)
            print("#########")



        ElevationScreen.onscreenclick(GetPos,btn = 1)
    
        #CartesianLine function
        def CartesianLineFunction():
            global Entities
            global buffer
            #get user inputs            
            if len(buffer) == 2: 
                x1 = buffer[0][0]
                y1 = buffer[0][1]
                x2 = buffer[1][0]
                y2 = buffer[1][1]
                

                #set starting position to write the line
                ElevationTurtle.penup()
                ElevationTurtle.setx(int(x1))
                ElevationTurtle.sety(int(y1))

               
                #drawing
                ElevationTurtle.pendown()
                ElevationTurtle.goto(int(x2),int(y2))
                
                #save entity
                Entities.append(["line",x1,y1,x2,y2])
                print(Entities)
                #for G CODE
                global GcodeCanvasIndex
                global EntitiesCanvasIndex
                GcodeLines.append("G01 X{} Y{}\n".format(x2,y2))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                #for Entities
                #EntitiesCanvas.insert(EntitiesCanvasIndex,Entities[int(EntitiesCanvasIndex)])
                #EntitiesCanvasIndex += 1
            else:
                messagebox.showinfo("Wrong input","Enter Only two Coordinates")

            buffer = []
            
            
      
         
        def dotproduct(v1, v2):
            return abs(v1[0]*v2[0])+(v1[1]*v2[1])
    
        def length(v):
            return math.sqrt(dotproduct(v, v))

        def angle(v1, v2):
            return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))*180/math.pi
        
        
        def ArcCircleFunction():

            global buffer
            #get user inputs
            x1 = buffer[0][0]
            y1 = buffer[0][1]
            x2 = buffer[1][0]
            y2 = buffer[1][1]
            #for point 1 and 2 to get the R
            dx = x1 - x2
            dy = y1 - y2
            R = math.sqrt(pow(dx,2)+pow(dy,2))



            #get the acute angle between vector 01 and 02     
            Angle = angle(buffer[2],buffer[1])
            
            #detect the the quadrant
            if buffer[2][0] > buffer[0][0] and buffer[2][1] > buffer[0][1]:
                Angle += 0
                quadrant = 1
            elif buffer[2][0] < buffer[0][0] and buffer[2][1] > buffer[0][1]:
                Angle += 90
                quadrant = 2
            elif buffer[2][0] < buffer[0][0] and buffer[2][1] < buffer[0][1]:
                Angle += 180
                quadrant = 3
            elif buffer[2][0] > buffer[0][0] and buffer[2][1] < buffer[0][1]:
                Angle += 270
                quadrant = 4
            
            
            print("Angle\n")
            print(Angle)
            print("quad\n")
            print(quadrant)       
            

            #set starting position to write the line
            ElevationTurtle.penup()
            ElevationTurtle.home()
            ElevationTurtle.setx(int(x2))
            ElevationTurtle.sety(int(y2))
           
            #drawing
            ElevationTurtle.pendown()
            ElevationTurtle.circle(R,Angle)

     
            #for G CODE     
            global GcodeCanvasIndex            
            I,J = ElevationTurtle.pos()        

            
            if Angle < 0:
                GcodeLines.append("G02 X{} Y{} I{} J{}\n".format(x1+(CanvasSizeX/2),y1+(CanvasSizeX/2),round(I+(CanvasSizeX/2),3),round(J+(CanvasSizeX/2)),3))
            
            elif Angle >= 0:
                GcodeLines.append("G03 X{} Y{} I{} J{}\n".format(x1+(CanvasSizeX/2),y1+(CanvasSizeX/2),round(I+(CanvasSizeX/2),3),round(J+(CanvasSizeX/2)),3))

            GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
            GcodeCanvasIndex+=1
                
                
        
            buffer = []
                    

         

        #Circle function
        def CircleFunction():
            global Entities
            global buffer
            if len(buffer) == 2: 

                #get user inputs
                x1 = buffer[0][0]
                y1 = buffer[0][1]
                x2 = buffer[1][0]
                y2 = buffer[1][1]
                #for point 1 and 2 to get the R
                dx = x1 - x2
                dy = y1 - y2
                R = math.sqrt(pow(dx,2)+pow(dy,2))
                Angle = 360

                #set starting position to write the line
                ElevationTurtle.penup()
                ElevationTurtle.home()
                startPosX = x1
                startPosY = y1-R
                ElevationTurtle.setx(int(startPosX))
                ElevationTurtle.sety(int(startPosY))
               
                #drawing
                ElevationTurtle.pendown()
                ElevationTurtle.circle(R,Angle)

                #save entity
                Entities.append(["circle",x1,y1,R,x2,y2])
                print(Entities)
                
                #for G CODE     
                global GcodeCanvasIndex            
                I,J = ElevationTurtle.pos()        

                

                GcodeLines.append("G03 X{} Y{} I{} J{}\n".format(x1+(CanvasSizeX/2),y1+(CanvasSizeY/2),round(I+(CanvasSizeX/2),3),round(J+(CanvasSizeY/2)),3))

                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
            else:
                messagebox.showinfo("Wrong input","Enter Only two Coordinates")

            buffer = [] 
                
        
        #Rectangle function
        def RectangleFunction():
            global Entities
            global buffer
            #get user inputs            
            if len(buffer) == 2: 
                x1 = buffer[0][0]
                y1 = buffer[0][1]
                x2 = buffer[1][0]
                y2 = buffer[1][1]
            
            

                #set starting position to write the line
                ElevationTurtle.penup()
                ElevationTurtle.home()
                ElevationTurtle.setx(int(x1))
                ElevationTurtle.sety(int(y1))
               
               
               
                #drawing first line
                ElevationTurtle.pendown()
                ElevationTurtle.goto(x2,y1)
                M,N = ElevationTurtle.pos()
                
                #save entity
                Entities.append(["line",x1,y1,x2,y1])
                
                #for G CODE
                global GcodeCanvasIndex
                GcodeLines.append("G01 X{} Y{}\n".format(M+(CanvasSizeX/2),N+(CanvasSizeY/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                
                       
                #drawing second line
                ElevationTurtle.pendown()
                ElevationTurtle.goto(x2,y2)
                M,N = ElevationTurtle.pos()

                
                #save entity
                Entities.append(["line",x2,y1,x2,y2])
                
                
                #for G CODE
                GcodeLines.append("G01 X{} Y{}\n".format(M+(CanvasSizeX/2),N+(CanvasSizeY/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                
                #drawing third line
                ElevationTurtle.pendown()
                ElevationTurtle.goto(x1,y2)
                M,N = ElevationTurtle.pos()
                
                #save entity
                Entities.append(["line",x2,y2,x1,y2])

                
                #for G CODE
                GcodeLines.append("G01 X{} Y{}\n".format(M+(CanvasSizeX/2),N+(CanvasSizeY/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
                #drawing fourth line
                ElevationTurtle.pendown()
                ElevationTurtle.goto(x1,y1)
                M,N = ElevationTurtle.pos()
                
                #save entity
                Entities.append(["line",x1,y2,x1,y1])
                print(Entities)
                
                #for G CODE
                GcodeLines.append("G01 X{} Y{}\n".format(M+(CanvasSizeX/2),N+(CanvasSizeY/2)))
                GcodeCanvas.insert(GcodeCanvasIndex,GcodeLines[int(GcodeCanvasIndex)])
                GcodeCanvasIndex+=1
                
            else:
                messagebox.showinfo("Wrong input","Enter Only two Coordinates")

            buffer = []
                
      
 
        
        def RotateFunction():
            global Entities

            arrEntities = []
            EntityNum = SelectedEntitiesEntry.get()
            """
            Set EntityNum to 1 because there is a bug 
            later maybe I will make the fucttion applicable to more that one entitiy
            
            """
            EntityNum = 1
            Angle = ValueAEntry.get()
            #save the entities to rotate
            for i in range(1,int(EntityNum)+1):
                arrEntities.append(Entities[-i])
                
            #delete the entities to rotate
            for i in range(1,int(EntityNum)+1):
                ElevationTurtle.undo()

            #draw the rotated enities
            for i in range(0,int(EntityNum)):
                if arrEntities[i][0] == 'line':
                    x1 = arrEntities[i][1]
                    y1 = arrEntities[i][2]
                    x2 = arrEntities[i][3]
                    y2 = arrEntities[i][4]
                    
                    #rotate algorithym

                    Angle =  int(float(Angle)*math.pi/180)
                    #step 1: move x2,y2 to origin
                    x2 -= x1
                    y2 -= y1

                    #step 2: Rotate
                    rotationMAT = np.array([[math.cos(Angle),-math.sin(Angle)],[math.sin(Angle),math.cos(Angle)]])
                    PointMAT = np.array([[x2],[y2]])

                    x2,y2 = rotationMAT.dot(PointMAT)

                    x2 += x1
                    y2 += y1

                    #draw the rotated line
                    #set starting position to write the line
                    ElevationTurtle.penup()
                    ElevationTurtle.setx(int(x1))
                    ElevationTurtle.sety(int(y1))
                  
                    #drawing
                    ElevationTurtle.pendown()
                    ElevationTurtle.goto(int(x2),int(y2))
                    Entities.pop()
                    Entities.append(["line",x1,y1,float(x2),float(y2)])
             
             
        def ScaleFunction():
                global Entities

                arrEntities = []
                EntityNum = SelectedEntitiesEntry.get()
                """
                Set EntityNum to 1 because there is a bug 
                later maybe I will make the fucttion applicable to more that one entitiy
                
                """
                EntityNum = 1
                a = int(ValueAEntry.get())
                b = int(ValueAEntry.get())
                
                if a>0 and b>0:
                    #save the entities to rotate
                    for i in range(1,int(EntityNum)+1):
                        arrEntities.append(Entities[-i])
                        
                    #delete the entities to rotate
                    for i in range(1,int(EntityNum)+1):
                        ElevationTurtle.undo()

                    #draw the rotated enities
                    for i in range(0,int(EntityNum)):
                        if arrEntities[i][0] == 'line':
                            x1 = arrEntities[i][1]
                            y1 = arrEntities[i][2]
                            x2 = arrEntities[i][3]
                            y2 = arrEntities[i][4]
                            

                            #step1: move x2,y2 to origin
                            x2 -= x1
                            y2 -= y1

                            #step 2: Scale
                            ScaleMAT = np.array([[a,0],[0,b]])
                            PointMAT = np.array([[x2],[y2]])

                            x2,y2 = ScaleMAT.dot(PointMAT)

                            x2 += x1
                            y2 += y1

                            #draw the rotated line
                            #set starting position to write the line
                            ElevationTurtle.penup()
                            ElevationTurtle.setx(int(x1))
                            ElevationTurtle.sety(int(y1))
                          
                            #drawing
                            ElevationTurtle.pendown()
                            ElevationTurtle.goto(int(x2),int(y2))
                            Entities.pop()
                            Entities.append(["line",x1,y1,float(x2),float(y2)])
                else:
                    messagebox.showinfo("Wrong input","Enter Value A and Value B")


        def TranslateFunction():
                global Entities

                arrEntities = []
                EntityNum = SelectedEntitiesEntry.get()
                """
                Set EntityNum to 1 because there is a bug 
                later maybe I will make the fucttion applicable to more that one entitiy
                
                """
                EntityNum = 1
                a = int(ValueAEntry.get())
                b = int(ValueBEntry.get())
                
                if a != "" and b != "":

                    #save the entities to rotate
                    for i in range(1,int(EntityNum)+1):
                        arrEntities.append(Entities[-i])
                        
                    #delete the entities to rotate
                    for i in range(1,int(EntityNum)+1):
                        ElevationTurtle.undo()

                    #draw the rotated enities
                    for i in range(0,int(EntityNum)):
                        if arrEntities[i][0] == 'line':
                            x1 = arrEntities[i][1]
                            y1 = arrEntities[i][2]
                            x2 = arrEntities[i][3]
                            y2 = arrEntities[i][4]
                            


                            #step 1: Translate
                            TranslateMAT = np.array([[1,0,a],[0,1,b],[0,0,1]])
                            PointMAT = np.array([[x2],[y2],[1]])

                            x2 = TranslateMAT.dot(PointMAT)[0]
                            y2 = TranslateMAT.dot(PointMAT)[1]

                            x1 += a
                            y1 += b
                            

                            #draw the rotated line
                            #set starting position to write the line
                            ElevationTurtle.penup()
                            ElevationTurtle.setx(int(x1))
                            ElevationTurtle.sety(int(y1))
                          
                            #drawing
                            ElevationTurtle.pendown()
                            ElevationTurtle.goto(int(x2),int(y2))
                            Entities.pop()
                            Entities.append(["line",x1,y1,float(x2),float(y2)])
                else:
                    messagebox.showinfo("Wrong input","Enter Value A and Value B")


                    
        def ExtrudeFunction():
                global Entities
                ElevationTurtle.width(10)
                ElevationTurtle.speed("fastest")
                arrEntities = []
                EntityNum = SelectedEntitiesEntry.get()

                a = int(ValueAEntry.get())
                
                if a > 0 :
                    #save the entities to rotate
                    for i in range(1,int(EntityNum)+1):
                        arrEntities.append(Entities[-i])

                    #draw the rotated enities
                    for i in range(0,int(EntityNum)):

                        if arrEntities[i][0] == 'line':
                            x1 = arrEntities[i][1]
                            y1 = arrEntities[i][2]
                            x2 = arrEntities[i][3]
                            y2 = arrEntities[i][4]
                            for j in range(a):
                                #Translate
                                x1 = arrEntities[i][1]+5*j
                                y1 = arrEntities[i][2]+8*j
                                x2 = arrEntities[i][3]+5*j
                                y2 = arrEntities[i][4]+8*j
                                    
                                
                                #set starting position to write the line
                                ElevationTurtle.penup()
                                ElevationTurtle.setx(int(x1))
                                ElevationTurtle.sety(int(y1))
                              
                                #drawing
                                ElevationTurtle.pendown()
                                ElevationTurtle.goto(int(x2),int(y2))
                                
                                
                        if arrEntities[i][0] == 'circle':
                            x1 = arrEntities[i][1]
                            y1 = arrEntities[i][2]
                            x2 = arrEntities[i][3]
                            y2 = arrEntities[i][4]
                            
                            for j in range(a):
                                #Translate
                                x1 = arrEntities[i][1]+5*j
                                y1 = arrEntities[i][2]+8*j
                                x2 = arrEntities[i][4]+5*j
                                y2 = arrEntities[i][5]+8*j
                                    
                                
                               #for point 1 and 2 to get the R
                                dx = x1 - x2
                                dy = y1 - y2
                                R = math.sqrt(pow(dx,2)+pow(dy,2))
                                Angle = 360

                                #set starting position to write the line
                                ElevationTurtle.penup()
                                ElevationTurtle.home()
                                ElevationTurtle.setx(int(x2))
                                ElevationTurtle.sety(int(y2))
                               
                                #drawing
                                ElevationTurtle.pendown()
                                ElevationTurtle.circle(R,Angle)
                        ElevationTurtle.penup()


                else:
                    messagebox.showinfo("Wrong input","Enter Value A")

                ElevationTurtle.width(1)


                
        def ExtrudeCutFunction():
                global Entities
                ElevationTurtle.width(10)
                ElevationTurtle.speed("fastest")
                ElevationTurtle.pencolor('gray')
                arrEntities = []
                EntityNum = SelectedEntitiesEntry.get()

                a = int(ValueAEntry.get())
                
                if a > 0 :
                    #save the entities to rotate
                    for i in range(1,int(EntityNum)+1):
                        arrEntities.append(Entities[-i])


                    #draw the rotated enities
                    for i in range(0,int(EntityNum)):

                        if arrEntities[i][0] == 'line':
                            x1 = arrEntities[i][1]
                            y1 = arrEntities[i][2]
                            x2 = arrEntities[i][3]
                            y2 = arrEntities[i][4]
                            for j in range(a):
                                #Translate
                                x1 = arrEntities[i][1]-5*j
                                y1 = arrEntities[i][2]-8*j
                                x2 = arrEntities[i][3]-5*j
                                y2 = arrEntities[i][4]-8*j
                                    
                                
                                #set starting position to write the line
                                ElevationTurtle.penup()
                                ElevationTurtle.setx(int(x1))
                                ElevationTurtle.sety(int(y1))
                              
                                #drawing
                                ElevationTurtle.pendown()
                                ElevationTurtle.goto(int(x2),int(y2))
                                
                                
                        if arrEntities[i][0] == 'circle':
                            x1 = arrEntities[i][1]
                            y1 = arrEntities[i][2]
                            x2 = arrEntities[i][3]
                            y2 = arrEntities[i][4]
                            
                            for j in range(a):
                                #Translate
                                x1 = arrEntities[i][1]-5*j
                                y1 = arrEntities[i][2]-8*j
                                x2 = arrEntities[i][4]-5*j
                                y2 = arrEntities[i][5]-8*j
                                    
                                
                               #for point 1 and 2 to get the R
                                dx = x1 - x2
                                dy = y1 - y2
                                R = math.sqrt(pow(dx,2)+pow(dy,2))
                                Angle = 360

                                #set starting position to write the line
                                ElevationTurtle.penup()
                                ElevationTurtle.home()
                                ElevationTurtle.setx(int(x2))
                                ElevationTurtle.sety(int(y2))
                               
                                #drawing
                                ElevationTurtle.pendown()
                                ElevationTurtle.circle(R,Angle)
                        ElevationTurtle.penup()


                else:
                    messagebox.showinfo("Wrong input","Enter Value A")

                ElevationTurtle.width(1)
                ElevationTurtle.pencolor('black')

                
                
                
                
                
        def ClearFunction() :
            ElevationTurtle.penup()
            ElevationTurtle.clear()
            ElevationTurtle.home()
             
             



         
         
        #optionMenu Drawings

        #cartesian line (needs x1, y1, x2, y2)
        CartLine = Button(window,text="Cartesian Line",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = CartesianLineFunction)
        CartLine.place(x=0,y=0)


        
        #Rectangle Circles (needs x1, y1, x2, y2)
        Rectangle = Button(window,text="Rectangle",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = RectangleFunction)
        Rectangle.place(x=100,y=0)


        #Circles (needs x1, y1, Reduis)
        Circle = Button(window,text="Circle",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = CircleFunction)
        Circle.place(x=200,y=0)
        
        
        #Arc Circles (needs x1, y1, Reduis, Angle)
        ArcCircle = Button(window,text="Arc",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2,state=DISABLED, command = ArcCircleFunction)
        ArcCircle.place(x=300,y=0)

        
        #Rotate (Entity, Value A: Angle)
        Rotate = Button(window,text="Rotate",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = RotateFunction)
        Rotate.place(x=400,y=0)

        
        #Scale (Entity, Value A :scale factor of x, Value B :scale factor of y)
        Scale = Button(window,text="Scale",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = ScaleFunction)
        Scale.place(x=100,y=45)
        
        
        #Translate (Entity, Value A :translate factor of x, Value B :translate factor of y)
        Translate = Button(window,text="Translate",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = TranslateFunction)
        Translate.place(x=200,y=45)
        
        
        
        #Extrude (Entity, Value A :translate factor of x, Value B :translate factor of y)
        Extrude = Button(window,text="Extrude",font='sans 8 bold',bg="tomato", bd = 5, width = 12, height = 2, command = ExtrudeFunction)
        Extrude.place(x=300,y=45)        
        


        #Extrude (Entity, Value A :translate factor of x, Value B :translate factor of y)
        Extrude = Button(window,text="Extrude Cut",font='sans 8 bold',bg="tomato", bd = 5, width = 12, height = 2, command = ExtrudeCutFunction)
        Extrude.place(x=400,y=45)        
                
        
        #Clear
        Clear = Button(window,text="Clear",font='sans 8 bold',bg="mediumpurple", bd = 5, width = 12, height = 2, command = ClearFunction)
        Clear.place(x=0,y=45)












        
        
        
        
        
        
        
        
        
        







#draw manual cartesian line
#drawLine(10,10,100,20,ElevationTurtle)

window.mainloop()