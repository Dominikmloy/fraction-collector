#raspberry
#!/usr/bin/python
import os
import sys
from time import *
import RPi.GPIO as GPIO
import threading

main_start=True
main_stop=False
##########################################################
# Verwendete Pins am Rapberry Pi
A=18
B=23
C=24
D=25
#Enable Treiber
AA=8
BB=7
#Stop-Button
STOP=27
#0.3sec ist sehr langsam -> ohne Fehler
#0.002sec ist ohne Fehler noch moeglich
s100 = 0.005
s75 = 0.01
s50 = 0.025
s25 = 0.05
s0  = 0.1
ticks = 0
# Pins aus Ausgange definieren
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(A,GPIO.OUT)
GPIO.setup(B,GPIO.OUT)
GPIO.setup(C,GPIO.OUT)
GPIO.setup(D,GPIO.OUT)
GPIO.setup(AA,GPIO.OUT)
GPIO.setup(BB,GPIO.OUT)
GPIO.setup(STOP, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.output(A, False)
GPIO.output(B, False)
GPIO.output(C, False)
GPIO.output(D, False)
GPIO.output(AA,True)
GPIO.output(BB,True)
out_pins = [A,B,C,D]
#links
mask_dl =[[1,0,1,0],
          [1,0,0,1],
          [0,1,0,1],
          [0,1,1,0]]
#rechts
mask_dr =[[0,1,1,0],
          [0,1,0,1],
          [1,0,0,1],
          [1,0,1,0]]
gesamt_teil_schritt = len(mask_dl)
#########################################################
#global variable
stop_xA=0
#########################################################
def stop_move(STOP):
    global stop_xA
    if GPIO.input(STOP)==0:##taster gedrueckt
        stop_xA=1
        print("STOP-Taste zu")
    else: ##taster offen
        stop_xA=0
        print("STOP-Taste offen")

GPIO.add_event_detect(STOP, GPIO.BOTH, callback=stop_move, bouncetime=200)
##########################################################
def main():
    try:
        os.system("clear")
        ticks=100 ## 200: one round
        move_initial(s25,s0)
        sleep(1)
        #move_left(ticks,s25)
        move_right(ticks,s25)
        GPIO.cleanup()
        main_start=True
        while main_start: ##wird noch nicht genutzt
            if main_stop==False:
                main_start=False
    except:
        GPIO.cleanup()
        return False

def move_initial (speed_l,speed_r):
    global stop_xA
    try:
        #1.Teil fahren(links) bis der Taster "gedrückt" stop
        count_teil_schritt=0
        while (not stop_xA):
            for pin in range(0,4): #Elemente in Mask
                pin_id=out_pins[pin] #Out Zuweisung
                if mask_dl[count_teil_schritt ][pin]!=0:
                    #print (" Enable GPIO %i" %(pin_id))
                    GPIO.output(pin_id, True)
                else:
                    GPIO.output(pin_id, False)
            count_teil_schritt  = count_teil_schritt  + 1
            if count_teil_schritt >= gesamt_teil_schritt: #Kompletter Schritt abgeschlossen(4Teilschritte)
                count_teil_schritt  = 0
            sleep(speed_l)
        sleep(0.5)
		#2.Teil fahren bis der Taster wieder "nicht gedrückt" dann 0 Position
        count_teil_schritt=0
        while (stop_xA):
            for pin in range(0,4): #Elemente in Mask
                pin_id=out_pins[pin] #Out Zuweisung
                if mask_dr[count_teil_schritt ][pin]!=0:
                    #print (" Enable GPIO %i" %(pin_id))
                    GPIO.output(pin_id, True)
                else:
                    GPIO.output(pin_id, False)
            count_teil_schritt  = count_teil_schritt  + 1
            if count_teil_schritt >= gesamt_teil_schritt: #Kompletter Schritt abgeschlossen(4Teilschritte)
                count_teil_schritt  = 0
            sleep(speed_r)
    except:
        GPIO.cleanup()
        print("x")
        return False

def move_left (ticks,speed):
	# Der Winkel enspricht 1,8Grad d.h dass bei 200 gesamtschritten(ist 1 seqenzdurchlauf) 360Grad erreicht sind
    try:
        count_teil_schritt=0
        for i in range(0,ticks):
            for pin in range(0,4): #Elemente in Mask
                pin_id=out_pins[pin] #Out Zuweisung
                if mask_dl[count_teil_schritt ][pin]!=0:
                    #print (" Enable GPIO %i" %(pin_id))
                    GPIO.output(pin_id, True)
                else:
                    GPIO.output(pin_id, False)
            count_teil_schritt  = count_teil_schritt  + 1
            if count_teil_schritt >= gesamt_teil_schritt: #Kompletter Schritt abgeschlossen(4Teilschritte)
                count_teil_schritt  = 0
            sleep(speed)
    except:
        GPIO.cleanup()
        return False

def move_right (ticks,speed):
	# Der Winkel enspricht 1,8Grad d.h dass bei 200 gesamtschritten(ist 1 seqenzdurchlauf) 360Grad erreicht sind
    try:
        count_teil_schritt=0
        for i in range(0,ticks):
            for pin in range(0,4): #Elemente in Mask
                pin_id=out_pins[pin] #Out Zuweisung
                if mask_dr[count_teil_schritt ][pin]!=0:
                    #print (" Enable GPIO %i" %(pin_id))
                    GPIO.output(pin_id, True)
                else:
                    GPIO.output(pin_id, False)
            count_teil_schritt  = count_teil_schritt  + 1
            if count_teil_schritt >= gesamt_teil_schritt: #Kompletter Schritt abgeschlossen(4Teilschritte)
                count_teil_schritt  = 0
            sleep(speed)
    except:
        GPIO.cleanup()
        return False
###########################################################################
if __name__ == '__main__':
      main()
sys.exit(0)
