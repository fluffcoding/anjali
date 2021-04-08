nmbrs='0123456789'
uc='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
spc='#$%'
sum=0;a=0;b=0;c=0;d=0
password=input('\nPlease enter your password:')

def passCheck(pas):
    for i in pas:
        if i in nmbrs or i in spc or i in uc:
            pass
        else: 
            print('pass not okay')
            password=input('\nPlease enter your password:')
            passCheck(password)
    print('pass accepted')
if len(password) >= 6:
    passCheck(password)
else: 
    print('password too short')
    password=input('\nPlease enter your password:')
    passCheck(password)