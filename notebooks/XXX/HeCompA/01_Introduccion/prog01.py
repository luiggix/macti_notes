
k = 1000 
L = 0.5  
TA = 100
TB = 500 
q = 0
N = 21

xlc = [L * i / N for i in range(0,N+1)]
T = []

for x in xlc:
    T.append( ((TB - TA)/L + q /(2*k) * (L - x) ) * x + TA )

print('Valores de x:', xlc)
print('Valores de T: {}'.format(T))