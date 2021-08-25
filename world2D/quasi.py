def corput(n,base):
    q,bk=0,1/base
    while(n>0):
        q+=(n %base)*bk
        n/=base
        bk/=base
    return q

for i in range(20):
    print(corput(i+1,10))	