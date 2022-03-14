cetrespetadecimal_tablica = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A' , 'B', 'C', 'D', 'E', 'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i']
decimal = int(input("Unesite broj: "))
cetrespetadecimal = ''
while(decimal>0):
    ostatak = decimal%45
    cetrespetadecimal= cetrespetadecimal_tablica[ostatak]+ cetrespetadecimal
    decimal = decimal//45
    
print("Cetrespetadecimal: ", cetrespetadecimal)