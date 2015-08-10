import serial
import time

# servo positions to move to the origin
origin = [140,82,115,145,149,0]

# servo positions to move to the center of the board
center = [80,5,118,151,176,95]

# servo positions when picking up the piece
# the arm hovers first and grabs the piece after
pickupHover = [
(140,31,133,161,166,33), #first move
(140,19,124,144,166,23), #second move
(140,49,131,137,149,47), #third move
(140,41,108,145,146,39)  #fourth move
]

pickupGrab = [
(140,31,128,164,138,33), #first move
(140,19,124,144,126,23), #second move
(140,49,135,137,122,47), #third move
(140,41,108,145,122,39)  #fourth move
]


# servo positions when placing the piece to the right region
# the arm hovers first and places the piece to the board after
dropHovers = [
(70,49,148,151,179,143), #region 1
(70,5,155,151,179,104),  #region 2
(70,55,148,151,175,60),  #region 3

(70,25,115,151,150,119), #region 4
(70,5,122,151,140,95),   #region 5
(70,74,125,151,160,70),  #region 6

(70,20,90,151,140,108),  #region 7
(70,5,98,151,135,92),    #region 8
(70,179,95,151,140,81)   #region 9
]

dropPuts = [
(70,39,145,152,135,133), #region 1
(70,15,145,165,140,104), #region 2
(70,55,145,151,130,60),  #region 3

(70,25,120,151,125,119), #region 4
(70,5,127,151,130,95),   #region 5
(70,74,127,151,130,70),  #region 6

(70,20,93,151,120,108),  #region 7
(70,5,98,151,120,92),    #region 8
(70,179,100,151,118,81)  #region 9

]

servo=['g','w','h','e','s','t']

class Arm():

    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baud = 9600

    def initialize(self):
        # Opens the serial port and moves the arm to the origin
        self.ser.open()
        self.goOrigin()

    def goOrigin(self):
        # Moves the arm to the origin
        "Moving to origin"
        for i in xrange(6):
            self.ser.write(str(origin[i]) + servo[i])
            time.sleep(0.10)

    def goCenter(self):
        # Moves the arm to the center of the board
        print "Moving to center..."
        for i in xrange(6):
            self.ser.write(str(center[i]) + servo[i])
            time.sleep(0.10)

    def pickHover(self,turn):
        # Moves the arm on top of the piece
        print "Finding block..."
        for i in xrange(6):
            self.ser.write(str(pickupHover[turn][i]) + servo[i])
            time.sleep(0.10)

    def pickGrab(self, turn):
        # Moves the arm towards the piece and grab
        print "Grabbing..."
        for i in xrange(6):
            self.ser.write(str(pickupGrab[turn][i]) + servo[i])
            time.sleep(0.10)

    def pickRecover(self, turn):
        # Moves the arm back to hover point after picking up the piece
        print "Recovering..."
        for i in xrange(6):
            if i == 0:
                self.ser.write(str(70) + 'g')
                time.sleep(0.10)
            else:
                self.ser.write(str(pickupHover[turn][i]) + servo[i])
                time.sleep(0.10)

    def dropHover(self,turn):
        # Moves the arm on top of the dropping point(region)
        print "Finding region", turn + 1
        for i in xrange(6):
            self.ser.write(str(dropHovers[turn][i]) + servo[i])
            time.sleep(0.10)

    def dropPut(self, turn):
        # Places the piece on the board
        print "Placing..."
        for i in xrange(6):
            self.ser.write(str(dropPuts[turn][i]) + servo[i])
            time.sleep(0.10)

    def dropRecover(self, turn):
        # Moves the arm back to the hover point after placing the piece on the board
        print "Recovering..."
        for i in xrange(6):
            if i == 0:
                self.ser.write(str(140) + 'g')
                time.sleep(0.10)
            else:
                self.ser.write(str(dropHovers[turn][i]) + servo[i])
                time.sleep(0.10)

    def grip(self):
        # Grips the piece
        print "Gripping..."
        self.ser.write("70g")
        time.sleep(0.10)

    def ungrip(self):
        # Ungrips the piece
        print "Ungripping..."
        self.ser.write("140g")
        time.sleep(0.10)

    def move(self, turn, region):
        # This runs the whole sequence from picking up the and dropping at the exact region

        time.sleep(1)
        self.pickHover(turn)
        time.sleep(1)

        self.pickGrab(turn)
        time.sleep(1)

        self.grip()
        time.sleep(1)

        self.pickRecover(turn)
        time.sleep(1)

        self.goCenter()
        time.sleep(1)

        self.dropHover(region)
        time.sleep(1)

        self.dropPut(region)
        time.sleep(1)

        self.ungrip()
        time.sleep(1)

        self.dropRecover(region)
        time.sleep(1)

        self.goOrigin()
        time.sleep(1)


if __name__ == "__main__":
    arm = Arm("/dev/ttyACM0")
    arm.initialize()
    arm.move(0,3)
