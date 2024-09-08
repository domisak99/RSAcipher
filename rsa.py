import sys
import random
import math
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
 
qtCreatorFile = "rsa.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class RSA(QMainWindow, Ui_MainWindow):

    def Convert(self, string): 
        li = list(string.split(" ")) 
        return li

    def UseData(self):
        pub=self.vere_klic.toPlainText()
        n=self.n_klic.toPlainText()
        priv=self.priv_klic.toPlainText()
        self.vstup_e.setText(str(pub))
        self.vstup_n.setText(str(n))
        self.vstup_d.setText(str(priv))
        self.vere_klic.clear()
        self.priv_klic.clear()
        self.n_klic.clear()

    def is_prime(self ,num):
        if num == 2:
            return True
        elif num < 2:
            return False
        elif num % 2 == 0:
            return False
        else:
            for i in range(3, int(math.sqrt(num)), 2):
                if num%i == 0:
                    return False
        return True


    def modular_inverse(self, a, m):
        m0 = m
        y = 0
        x = 1
        if (m == 1):
            return 0
        
        while (a > 1):
            q = a // m
            t = m


            m = a % m
            a = t
            t = y


            y = x - q * y
            x = t


        if (x < 0):
            x = x + m0
        return x


    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a


    def generate_keys(self):
        p = random.randint(1e3, 1e5)
        while not self.is_prime(p):
            p = random.randint(1e3, 1e5)
        q = random.randint(1e3, 1e5)
        while not self.is_prime(q):
            q = random.randint(1e3, 1e5)
        n = p*q
        phi = (p-1)*(q-1)
        e = random.randint(1, phi)
        while self.gcd(e, phi) != 1:
            e = random.randint(1, phi)
        d = self.modular_inverse(e, phi)
        return p, q, e, d


    def encrypt(self):
        p, q, pub, priv = self.generate_keys()
        n = p*q
        plain=self.vstup.toPlainText()
        cipher = []
        for char in plain:
            a = ord(char)
            cipher.append(pow(a, pub, n))
        str1 = " ".join(map(str,cipher))
        self.vystup.setText(str1)
        self.vere_klic.setText(str(pub))
        self.n_klic.setText(str(n))
        self.priv_klic.setText(str(priv))
        return cipher


    def decrypt(self):
        plain = ''
        cip_input=self.vstup.toPlainText()
        cipher=self.Convert(cip_input)
        n=self.vstup_n.toPlainText()
        priv=self.vstup_d.toPlainText()
        for num in cipher:
            a = pow(int(num), int(priv), int(n))
            plain = plain + str(chr(a))
        self.vystup.setText(str(plain))
        return plain

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.T_sifrovat.clicked.connect(self.encrypt)
        self.T_desifrovat.clicked.connect(self.decrypt)
        self.T_pouzit.clicked.connect(self.UseData)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSA()
    window.show()
    sys.exit(app.exec_()) 
