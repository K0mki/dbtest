import sys

cetrespetadecimal_tablica = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A' , 'B', 'C', 'D', 'E', 'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i']

if len(sys.argv)<2:
    print(f'use {sys.argv[0]} number')
    sys.exit()

try:
    decimal = int(sys.argv[1])
except:
    print(f'invalid parameter, use integer')
    sys.exit()
    
cetrespetadecimal = ''
while(decimal>0):
    ostatak = decimal%45
    cetrespetadecimal= cetrespetadecimal_tablica[ostatak]+ cetrespetadecimal
    decimal = decimal//45
    
print("Cetrespetadecimal: ", cetrespetadecimal)