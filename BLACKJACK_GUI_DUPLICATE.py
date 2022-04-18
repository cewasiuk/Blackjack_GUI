#BLACKJACK_GUI_DUPLICATE
#04/18/22

from tkinter import *
import numpy as np 
import matplotlib.pyplot as plt 
import os 
import csv 
import pandas as pd
from csv import DictReader
savepath = "/Users/chrisewasiuk/Desktop/"
filename = "Blackjack_stats.csv"

complete_name = os.path.join(savepath, filename)

f = open(complete_name,"a")

writer = csv.writer(f)
col_list = ["Wins","Losses","Draws", "Hands", "Sum"]
#writer.writerow(col_list)


################################### Get Card Function ######################################

def getcard():
    card = np.random.randint(1,14)
    ctext = str(card)

    if card == 11: 
        ctext = 'Ace'
        return [card, ctext] 

    elif card == 12: 
        ctext = 'King'
        card = 10 
        return [card, ctext]

    elif card == 13: 
        ctext = 'Queen'
        card = 10
        return [card, ctext] 

    elif card == 1: 
        ctext = 'Jack'
        card = 10 
        return [card, ctext] 
    else:
        return [card, ctext]

################################# Window Display ###################################
dct = {}
lossdct = {}
pushdct = {}
for i in range(1,22):
    lossdct['init_loss%s' % i] = 0
    pushdct['init_push%s' % i] = 0
    dct['init_hand%s' % i] = 0

begin_count =[] 


class MyWindow:
    def __init__(self, win):



        #For data analysis of games 

        self.player = [] 
        self.dealer = [] 
        self.hitcount = [3]
        self.dhitcount = [3]

        self.lbl1=Label(win, text='Player')
        self.lbl1.place(x=100, y=100)

        self.lbl2=Label(win, text='Dealer')
        self.lbl2.place(x=725, y=100)


        #Player Card1
        self.card1l=Label(win, text='Card 1')
        self.card1l.place(x=50, y=250)
        self.c1=Entry(bd=1)
        self.c1.place(x=100, y= 250)

        #Player Card2
        self.card2l=Label(win, text='Card 2')
        self.card2l.place(x=50, y=300)
        self.c2=Entry(bd=1)
        self.c2.place(x=100, y= 300)

        #Player Card i 
        self.card3l=Label(win, text='Card {}'.format(sum(self.hitcount)))
        self.card3l.place(x=170, y=450)
        self.c3=Entry(bd=1)
        self.c3.place(x=100, y= 475)
        
        #Dealer Card1
        self.dcard1l=Label(win, text='Card 1')
        self.dcard1l.place(x=675, y=250)
        self.d1=Entry(bd=1)
        self.d1.place(x=725, y= 250)

        #Dealer Card2
        self.dcard2l=Label(win, text='Card 2')
        self.dcard2l.place(x=675, y=300)
        self.d2=Entry(bd=1)
        self.d2.place(x=725, y= 300)

        #Dealer Card i 
        b = 3
        self.dcard3l=Label(win, text='Card {}'.format(sum(self.dhitcount)))
        self.dcard3l.place(x=790, y=355)
        self.d3=Entry(bd=1)
        self.d3.place(x=725, y= 375)

        #Player Sum
        self.psuml=Label(win, text='Sum')
        self.psuml.place(x=50, y=150)
        self.psum=Entry(bd=1)
        self.psum.place(x=100, y= 150)

        #Dealer Sum
        self.dsuml=Label(win, text='Sum')
        self.dsuml.place(x=685, y=150)
        self.dsum=Entry(bd=1)
        self.dsum.place(x=725, y= 150)

        #Game Label 
        
        self.blackjack = Label(win, text = 'BLACKJACK', font = ('Times', 40))
        self.blackjack.place(x = 685, y = 500)

################################## BUTTONS ###################################

        #Begin Button
        self.hit=Button(win, text='BEGIN', width = 7, command = self.begin ) 
        self.hit.place(x=460, y=100)

        #Hit Button
        self.hit=Button(win, text='HIT', width = 3, command = None) 
        self.hit.place(x=110, y=375)

        #Stay Button
        self.stay=Button(win, text='STAY', width = 3, command = None)
        self.stay.place(x=215, y=375)

        #Plot Button
        self.plot=Button(win, text='ANALYSIS', width = 8, command = self.bargraph)
        self.plot.place(x=760, y=425)

################################## Initial Game Start ###################################

    def begin(self):
        self.player.clear()
        self.dealer.clear()
        self.hitcount.clear()
        self.dhitcount.clear()
        self.dhitcount.append(2)
        self.hitcount.append(2)
        self.hit["command"] = self.nextcard
        self.stay["command"] = self.hold

        self.card3l["text"]= 'Card {}'.format(3)
        self.dcard3l["text"]= 'Card {}'.format(3)

        self.blackjack["text"] = 'BLACKJACK' 

        self.psum.delete(0, 'end')
        self.dsum.delete(0, 'end')
        self.d1.delete(0, 'end')
        self.d2.delete(0, 'end')
        self.d3.delete(0, 'end')
        self.c1.delete(0, 'end')
        self.c2.delete(0, 'end')
        self.c3.delete(0, 'end')
    
        card1, ctext1 = getcard()
        card2, ctext2 = getcard()
        dealer1, dtext1 = getcard()

        #List Appending
        self.player.append(card1)
        self.player.append(card2)
        self.dealer.append(dealer1)

        #Rare case of two aces off the draw
        if sum(self.player) > 21:
            self.player[1] = 1

        #Card Text Boxes
        self.c1.insert(END, str(ctext1))
        self.c2.insert(END, str(ctext2))
        self.d1.insert(END, str(dtext1))
        self.d2.insert(END, '???')

        #Sum Appending
        self.psum.insert(END,str(sum(self.player)))
        self.dsum.insert(END,self.dealer)

################################# Hit Function ####################################

    def nextcard(self):
         
        self.hitcount.append(1)
        self.card3l["text"] = 'Card {}'.format(sum(self.hitcount)) 

        #Card i get()
        card3, ctext3 = getcard()
        self.c3.delete(0,'end')
        self.c3.insert(END, str(ctext3))
        self.player.append(card3)

        #Accounts for Ace being 1 or 11
        if sum(self.player) > 21:
            for i in range(0,len(self.player)):
                if self.player[i] == 11:
                    self.player[i] = 1
                    break

        #Changes Values before appending
        self.psum.delete(0, 'end')
        self.psum.insert(END,str(sum(self.player)))


        if sum(self.player) > 21: 
            self.blackjack["text"] = 'You Lose!' 
            self.hit["command"] = 'None'
            self.stay["command"] = 'None'
            begin_count.append(1)
            self.d2.delete(0,'end')
            self.dsum.delete(0,'end')
            dcard2, dctext2 = getcard()
            self.d2.insert(END, str(dctext2))
            self.dealer.append(dcard2)
            self.dsum.insert(END, sum(self.dealer))
            f = open(complete_name,"a")
            data = ["0", "1", "0", "1",(self.player[0] + self.player[1])]
            writer.writerow(data)

        
################################# Stay Function #########################################


#Look into coding case where dealer gets aces and goes over 

    def hold(self):

        begin_count.append(1)
        self.hit["command"] = 'None'
        self.stay["command"] = 'None'
        self.d2.delete(0,'end')
        self.dsum.delete(0,'end')
        dcard2, dctext2 = getcard()
        self.d2.insert(END, str(dctext2))
        self.dealer.append(dcard2)
        self.dsum.insert(END, sum(self.dealer))

        if sum(self.dealer) > 21:
            self.dealer[1] = 1 

        while sum(self.dealer) < 17:

            if sum(self.dealer) > 21:
                for i in range(0,len(self.dealer)):
                    if self.dealer[i] == 11:
                        self.dealer[i] = 1
                        break

            
            self.dhitcount.append(1)
            self.dcard3l["text"] = 'Card {}'.format(sum(self.dhitcount))
            dcard3, dctext3 = getcard()
            self.d3.delete(0,'end')
            self.d3.insert(END, str(dctext3))
            self.dealer.append(dcard3)
            self.dsum.delete(0,'end')
            self.dsum.insert(END, sum(self.dealer))

        if sum(self.dealer) > 21:
            self.blackjack["text"] = 'You Win!' 
            data = ["1", "0", "0", "1",(self.player[0] + self.player[1])]
            writer.writerow(data)
            
        
        elif sum(self.dealer) >= 17 and sum(self.player) > sum(self.dealer): 
            self.blackjack["text"] = 'You Win!' 
            f = open(complete_name,"a")
            data = ["1", "0", "0", "1",(self.player[0] + self.player[1])]
            writer.writerow(data)

                 
        elif sum(self.dealer) >= 17 and sum(self.player) < sum(self.dealer): 
            self.blackjack["text"] = 'You Lose!' 
            f = open(complete_name,"a")
            data = ["0", "1", "0", "1",(self.player[0] + self.player[1])]
            writer.writerow(data)

        
        elif sum(self.dealer) >= 17 and sum(self.player) == sum(self.dealer): 
            self.blackjack["text"] = 'Push, try again!' 
            f = open(complete_name,"a")
            data = ["0", "0", "1", "1",(self.player[0] + self.player[1])]
            writer.writerow(data)

        

################################## Plot Function ###############################

    def bargraph(self):

        for i in range(1,22):
            lossdct['init_loss%s' % i] = 0
            pushdct['init_push%s' % i] = 0
            dct['init_hand%s' % i] = 0
        hand = []
        wins = []
        loss = []
        push = []

        
        with open(complete_name,'r') as df1:
            csv_dict_reader = DictReader(df1)

            for row in  csv_dict_reader:
                total = int(row['Sum'])
                
                dct["init_hand{}".format(total)] += int(row['Wins'])
                lossdct["init_loss{}".format(total)] += int(row['Losses'])
                pushdct["init_push{}".format(total)] += int(row['Draws'])



        lossmax = 0
        winmax = 0
        width = 0.35

        for i in range(4,22):
            hand.append(i)
            wins.append(dct["init_hand{}".format(i)])
            loss.append(lossdct["init_loss{}".format(i)])
            push.append(pushdct["init_push{}".format(i)])
            
        for i in range(0,len(wins)):
            if wins[i] > winmax:
                winmax = wins[i] +loss[i] + push[i]

        for j in range(0,len(loss)):
            if loss[j] > lossmax:
                lossmax = loss[j] + wins[j] +push[j]
    
        max = 0 
        if lossmax > winmax:
            max = lossmax + 2 
        elif winmax > lossmax:
            max = winmax + 2
        elif winmax == lossmax:
            max = winmax + 2

        plt.bar(hand,wins,width)
        plt.bar(hand,loss,width, bottom = wins, color = 'red')
        plt.bar(hand,push,width, bottom = wins, color = 'orange') 


        plt.ylabel("Wins")
        plt.xlabel("Initial Hand Sum")
        plt.title('Hands Played: {}, Win Percentage = {} %'.format((sum(wins)+sum(loss)+sum(push)), round((100 * sum(wins))/(sum(wins)+ sum(loss)), 2)))
        plt.ylim([0,max])
        plt.xticks(np.arange(4,22,step = 1))
        plt.legend(['Wins: {}'.format(sum(wins)),'Losses: {}'.format(sum(loss)), 'Pushes: {}'.format(sum(push))])
        plt.show()

##################################################################################

window=Tk()
mywin=MyWindow(window)
window.title('Blackjack')
window.geometry("1000x600+10+10")
window.mainloop()
