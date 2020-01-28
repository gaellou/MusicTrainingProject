import time
import os

def main():
        while 1:
                # the _variable_ listing...
                # "n" is throw away integer number and purposely reused.
                # "beatstring" is the inputted string and is also reused.
                # "beat" is the floating point number from about 0.x to 1.x generated from the inputted data.
                #
                # The standard Linux clear screen cmmand.
                n=os.system("clear")
                # Set up a basic user screen/window.
                print("\nPython 3.x.x simple metronome for the Linux platform.\n")
                print("(C)2007-2012, B.Walker, G0LCU. Issued as Public Domain.\n")
                beatstring=input("Enter any whole number from 30 to 400 (bpm), (QUIT or EXIT to Quit):- ")
                # Allow a means of quitting the DEMO.
                if beatstring=="QUIT" or beatstring=="EXIT": break
                # Don't allow any errors...
                if len(beatstring)>=4: beatstring="100"
                if len(beatstring)<=1: beatstring="100"
                n=0
                while n<=(len(beatstring)-1):
                        if beatstring[n]>=chr(48) and beatstring[n]<=chr(57): n=n+1
                        else: beatstring="100"
                n=int(beatstring)
                if n<=30: n=30
                if n>=400: n=400
                # Convert this integer "n" back to the "beatstring" string...
                beatstring=str(n)
                # Now convert to the floating point value for the time.sleep() function.
                beat=((60/n)-0.125)
                print("\nApproximate beats per minute = "+beatstring+"...\n")
                print("Press Ctrl-C to enter another speed...")
                while 1:
                        # Write directly to the /dev/dsp device.
                        try:
                                audio=open("Sound/250551__druminfected__metronomeup.wav", "wb")
                                audio.write(b"\x00\xFF")
                                audio.close()
                                time.sleep(beat)
                        # There is a flaw here, I'll let you big guns find it... ;o)
                        # Note it is NOT really a bug!
                        except KeyboardInterrupt: break
main()
