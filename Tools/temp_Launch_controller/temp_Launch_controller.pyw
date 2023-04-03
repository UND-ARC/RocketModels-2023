from PyQt5.QtWidgets import *;
from PyQt5.QtCore import *;
from PyQt5.QtGui import *;
from screeninfo import get_monitors as getMonitors;
from constants import *;

import sys;
import serial;
import time;
import threading;

class App (QApplication):

    def __init__(self, args):
        # Application Initialization

        super().__init__(args);

        self.var = {
            ARM_FLAG               : False,
            ARM_BTN                : None,
            RSSI                   : None,
            CONT_LIGHTS            : None,
            CURR_BTN               : None,
            DEFAULT_WINDOW_SIZE    : None,
            FIRE_BTN               : None,
            MAIN_GRID              : None,
            RADIO_BTNS             : None,
            SCREEN_SIZE            : None,
            WINDOW                 : None,
            WINDOW_CENTER          : None,
        };

        self.setStyle('Fusion');
        self.var[SCREEN_SIZE] = self.getScreenSize();

        self.var[WINDOW] = QWidget();
        self.windowSetup(self.var[SCREEN_SIZE]);
        self.GUISetup();

        self.var[WINDOW].show();
        
        try:
             self.conn = serial.Serial('COM9', 115200);
        except Exception as serialError:
             print(f'\nError: {serialError}\n');
             sys.exit();
        
        # Continuity Setup
        #self.cont_thread = threading.Thread(target=self.continuity, args=[], daemon=True);
        self.recv_thread = threading.Thread(target=self.recv, args=[], daemon=True);
        #self.cont_thread.start();
        self.recv_thread.start();
        
        self.cont_thread = threading.Thread(target=self.contCheck, args=[], daemon=True);
        self.cont_thread.start();
        return;

    def ARM (self):
        arm_btn = self.var[ARM_BTN];
        fire_btn = self.var[FIRE_BTN];
        if ( (self.var[ARM_FLAG] == False) and (self.var[CURR_BTN] != None) ):
            arm_btn.setStyleSheet('font-size: 50px; font-weight: bold; background-color: green;');
            self.var[ARM_FLAG] = True;
            fire_btn.setDisabled(False);
        return;
    
    def FIRE (self):
        try:
            if ( (self.var[ARM_FLAG] == True) and (self.var[CURR_BTN] != None) ):
                self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: green;');
                match self.var[CURR_BTN].text().strip():
                    case '1':
                        print('1');
                        self.conn.write('FIRE 0\n'.encode());
                        self.var[FIRE_BTN].setDisabled(True);
                        time.sleep(2);
                        self.var[ARM_FLAG] = False;
                        self.var[ARM_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
                        self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
                        return;
                    case '2':
                        print('2');
                        self.conn.write('FIRE 1\n'.encode());
                        self.var[FIRE_BTN].setDisabled(True);
                        time.sleep(2);
                        self.var[ARM_FLAG] = False;
                        self.var[ARM_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
                        self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
                        return;
                    case '3':
                        print('3');
                        self.conn.write('FIRE 2\n'.encode());
                        self.var[FIRE_BTN].setDisabled(True);
                        time.sleep(2);
                        self.var[ARM_FLAG] = False;
                        self.var[ARM_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
                        self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
                        return;
                    case '4':
                        print('4');
                        self.conn.write('FIRE 3\n'.encode());
                        time.sleep(2);
                        self.var[ARM_FLAG] = False;
                        self.var[ARM_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
                        self.var[FIRE_BTN].setDisabled(True);
                        self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
                        return;
        except Exception as e:
            print(e)
            return;
        
    def contCheck(self):
        while True:
            time.sleep(5)
            self.conn.write('CONT\n'.encode());
            
    def recv(self):
        while True:
            try:
                data = self.conn.readline().decode();
                print("RECV:", data)
                if data[0] == '[':
                    data = data[1:-1];
                    i = 0;
                    for i in range(0, 4):
                        if data[i] == 'C':
                            self.var[CONT_LIGHTS][i].setStyleSheet('font-size: 20px; font-weight: bold; background-color: blue;');
                        else:
                            self.var[CONT_LIGHTS][i].setStyleSheet('font-size: 20px; font-weight: bold;');
                        i += 1;
                                
                elif data[0] == 'R':
                    _, rssi = data.split(' ');
                    self.var[RSSI].setText(rssi)
            except TypeError:
                pass
                    
    def continuity (self):
        self.conn.write('CONT\n'.encode());

    def centerWindow (self, offsetW = 0, offsetH = 0, singleOffset = 0):
        # Centers the Main Window based off of the offset values above,
        # 'singleOffset' Applies one Offset Value to both Width and Height is used,
        # 'offsetW' only Applies Value to Width; Similar with 'offsetH' and Height.

        windowCenter = self.var[WINDOW_CENTER];
        if (singleOffset != 0):
            singleOffset = singleOffset // 2;
            self.var[WINDOW].move(windowCenter[0] - singleOffset, windowCenter[1] - singleOffset);
        elif ( (offsetW != 0) or (offsetH != 0) ):
            offsetW = offsetW // 2; offsetH = offsetH // 2;
            self.var[WINDOW].move(windowCenter[0] - offsetW, windowCenter[1] - offsetH);
        else:
            self.var[WINDOW].move(windowCenter[0], windowCenter[1]);
        return;

    def currButton1 (self):
        try:
            btn_one = self.getButton('1');
            
            btn_one.setStyleSheet('font-size: 20px; font-weight: bold; background-color: orange;');
            self.setOtherBtns(btn_one);
            
            self.var[ARM_FLAG] = False;
            self.var[ARM_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
            self.var[FIRE_BTN].setDisabled(True);
            self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
            
            self.var[CURR_BTN] = btn_one;
        except:
            return;
    
    def currButton2 (self):
        try:
            btn_two = self.getButton('2');
        
            btn_two.setStyleSheet('font-size: 20px; font-weight: bold; background-color: orange;');
            self.setOtherBtns(btn_two);
        
            self.var[ARM_FLAG] = False;
            self.var[ARM_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
            self.var[FIRE_BTN].setDisabled(True);
            self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
        
            self.var[CURR_BTN] = btn_two;
        except:
            return;
    
    def currButton3 (self):
        try:
            btn_three = self.getButton('3');
            
            btn_three.setStyleSheet('font-size: 20px; font-weight: bold; background-color: orange;');
            self.setOtherBtns(btn_three);
            
            self.var[ARM_FLAG] = False;
            self.var[ARM_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
            self.var[FIRE_BTN].setDisabled(True);
            self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
            
            self.var[CURR_BTN] = btn_three;
        except:
            return;
    
    def currButton4 (self):
        try:
            btn_four = self.getButton('4');
            
            btn_four.setStyleSheet('font-size: 20px; font-weight: bold; background-color: orange;');
            self.setOtherBtns(btn_four);
            
            self.var[ARM_FLAG] = False;
            self.var[ARM_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
            self.var[FIRE_BTN].setDisabled(True);
            self.var[FIRE_BTN].setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
            
            self.var[CURR_BTN] = btn_four;
        except:
            return;

    def error (self, message):
        # Displays error window with chosen message.
        
        try:
            alert = QMessageBox();
            alert.setWindowTitle('Alert');
            alert.setText(message);
            alert.exec();
        except:
            return;

    def getACK (self):
        try:
            dataIn = self.conn.read(1024).decode();
            if ( not('ACK' in dataIn.strip()) ):
                self.error('No ACK!');
        except:
            return;

    def getButton(self, name):
        # Finds a specific button,
        # returns that button, if not, returns None.
        
        try:
            for button in self.var[RADIO_BTNS]:
                if (button.text() == name):
                    return button;
            return None;
        except:
            return None;

    def getScreenSize (self):
        # Scans all Connected Moniters and Gets Size of the Primary Monitor,
        # returns [width, height].

        monitor_info = [];
        for m in getMonitors():
            if (m.is_primary):
                if ( (m.width > 1920) and (m.height > 1080) ):
                    return [1920, 1080];
                monitor_info.append(m.width);
                monitor_info.append(m.height);
                return monitor_info;

    def GUISetup (self):
        # Sets up GUI with all Elements within i.e. Images, Buttons, etc...

        # Main Grid Setup
        mainGrid = QGridLayout();
        self.var[WINDOW].setLayout(mainGrid);

        # Sub-widget(s) Setup
        selector_btn_layout = QHBoxLayout();
        cont_light_layout = QHBoxLayout();
        rssi_layout = QHBoxLayout();
        
        mainGrid.addLayout(cont_light_layout, 3, 2, 1, 4);
        mainGrid.addLayout(selector_btn_layout, 4, 2, 1, 4);
        mainGrid.addLayout(rssi_layout, 1, 6, 1, 1);

        # Add Button(s) to GUI
        arm_btn = QPushButton('ARM');
        
        fire_btn = QPushButton('FIRE');
        
        btn_one = QPushButton('1');
        btn_two = QPushButton('2');
        btn_three = QPushButton('3');
        btn_four = QPushButton('4');        
        
        cont_box_one = QPushButton('CONT_1');
        cont_box_two = QPushButton('CONT_2');
        cont_box_three = QPushButton('CONT_3');
        cont_box_four = QPushButton('CONT_4');
        
        check_cont = QPushButton('Check CONT');

        # - Add Buttons to Layouts
        mainGrid.addWidget(arm_btn, 1, 2, 1, 4, alignment=Qt.AlignCenter);
        self.var[ARM_BTN] = arm_btn;
        
        mainGrid.addWidget(fire_btn, 2, 2, 1, 4, alignment=Qt.AlignCenter);
        self.var[FIRE_BTN] = fire_btn;
        
        mainGrid.addWidget(check_cont, );
        
        radioButtons = [];
        selector_btn_layout.addWidget(btn_one); radioButtons.append(btn_one);
        selector_btn_layout.addWidget(btn_two); radioButtons.append(btn_two);
        selector_btn_layout.addWidget(btn_three); radioButtons.append(btn_three);
        selector_btn_layout.addWidget(btn_four); radioButtons.append(btn_four);
        
        cont_lights = [];
        cont_light_layout.addWidget(cont_box_one); cont_lights.append(cont_box_one);
        cont_light_layout.addWidget(cont_box_two); cont_lights.append(cont_box_two);
        cont_light_layout.addWidget(cont_box_three); cont_lights.append(cont_box_three);
        cont_light_layout.addWidget(cont_box_four); cont_lights.append(cont_box_four);
        
        # Set Sizes for all Btns
        arm_btn.setFixedSize(300, 200);
        arm_btn.setStyleSheet('font-size: 50px; font-weight: bold; background-color: yellow;');
        
        fire_btn.setFixedSize(300, 200);
        fire_btn.setStyleSheet('font-size: 50px; font-weight: bold; background-color: red;');
        self.var[FIRE_BTN].setDisabled(True);
        
        check_cont.setFixedSize(100, 25);
        
        for button in cont_lights:
            button.setFixedSize(150, 50);
            button.setStyleSheet('font-size: 20px; font-weight: bold;');
            button.setDisabled(True);
        self.var[CONT_LIGHTS] = cont_lights;
        
        for button in radioButtons:
            button.setFixedSize(100, 25);
            button.setStyleSheet('font-size: 20px; font-weight: bold;');
        self.var[RADIO_BTNS] = radioButtons;
        
        # - Connect Buttons to Events
        arm_btn.clicked.connect(self.ARM);
        
        fire_btn.clicked.connect(self.FIRE);
        
        check_cont.clicked.connect(self.continuity);
        
        btn_one.clicked.connect(self.currButton1);
        btn_two.clicked.connect(self.currButton2);
        btn_three.clicked.connect(self.currButton3);
        btn_four.clicked.connect(self.currButton4);
        
        # Text Box
        rssiTextBox = QLineEdit();
        rssiTextBox.setFixedSize(150, 30);
        rssiTextBox.setText('None');
        rssiTextBox.setStyleSheet('font-size: 20px; font-weight: bold;');
        rssiTextBox.setDisabled(True);
        
        label = QLabel();
        label.setText('RSSI');
        label.setFixedSize(50, 25);
        label.setStyleSheet('font-size: 20px; font-weight: bold;');
        
        rssi_layout.addWidget(label);
        rssi_layout.addWidget(rssiTextBox);
        
        self.var[RSSI] = rssiTextBox;

        # Finalizing Objects
        self.var[MAIN_GRID] = mainGrid;
        return;

    def resizeWindow (self, offsetW = 0, offsetH = 0, singleOffset = 0):
        # Resizes main window based off off the offset given,
        # 'singleOffset' Applies one Offset Value to both Width and Height is used,
        # 'offsetW' only Applies Value to Width; Similar with 'offsetH' and Height.

        if (singleOffset != 0):
            self.var[WINDOW].resize(self.var[DEFAULT_WINDOW_SIZE][0] + singleOffset, self.var[DEFAULT_WINDOW_SIZE][1] + singleOffset);
        elif ( (offsetW != 0) or (offsetH != 0) ):
            self.var[WINDOW].resize(self.var[DEFAULT_WINDOW_SIZE][0] + offsetW, self.var[DEFAULT_WINDOW_SIZE][1] + offsetH);
        
        self.centerWindow(offsetW = offsetW, offsetH = offsetH, singleOffset=singleOffset);
        return;

    def setOtherBtns (self, btnToAvoid):
        try:
            for button in self.var[RADIO_BTNS]:
                if (button != btnToAvoid):
                    button.setStyleSheet('font-size: 20px; font-weight: bold;');
        except:
            return;

    def windowSetup (self, screen_sizes):
        # Sets up main window.

        # Set Window Title
        self.var[WINDOW].setWindowTitle("Launch Controller GUI");

        # Default Window Settings
        self.var[DEFAULT_WINDOW_SIZE] = [screen_sizes[0] // 2, screen_sizes[1] // 2];
        windowSize = self.var[DEFAULT_WINDOW_SIZE];
        self.var[WINDOW].setMinimumSize(windowSize[0], windowSize[1]);
        self.var[WINDOW].setMaximumSize(windowSize[0] * 2, (windowSize[1] * 2) - 75);
        self.var[WINDOW].setBaseSize(windowSize[0], windowSize[1]);
        self.var[WINDOW].setWindowFlags(Qt.WindowFlags());
        self.var[WINDOW].setWindowFlag(Qt.WindowMaximizeButtonHint, True);
        self.var[WINDOW].showMaximized();
        #self.var[WINDOW].setStyleSheet('position: absolute; left: 0px; top: 0px; z-index: top;');
        
        test = QWidget();
        test.setMaximumHeight(500);

        # Set Window to Center of the Screen
        centerpoint = QDesktopWidget().availableGeometry().center();
        self.var[WINDOW_CENTER] = [centerpoint.x() // 2, centerpoint.y() // 2];
        #self.centerWindow();
        return;

def main ():
    app = App([]);
    app.exec();
    return;

if (__name__ == "__main__"):
    main();
