import os
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import time
path = os.getcwd()
path = path[0:len(path) - 20]
listt = os.listdir(path + 'Imagens/')[0:680]
start = time.time()
fig = plt.figure(figsize=(20, 10))
im = []
plt.axis(False)
aux = True
for i in range(len(listt)):
    im.append([plt.imshow(plt.imread(os.getcwd()[:47] + 'Imagens/' + str(i) + '.png'))])
    if aux:
        stop = time.time()
        print((stop-start) * len(listt) / 60)
        aux = False

    

anim = ArtistAnimation(fig, im, interval=20)
anim.save(os.getcwd()[:47] + 'Simulação.gif', fps = 5)
#plt.show()
plt.close()
