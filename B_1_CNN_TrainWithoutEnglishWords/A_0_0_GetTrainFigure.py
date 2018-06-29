import requests




url = 'http://railway.hinet.net/ImageOut.jsp?pageRandom=0.05032386372934927'

for ii in range(0,100):
    
    res = requests.get(url)
    saveName = 'Train' + str(ii) + '.jpg'
    with open(saveName,'wb') as f:
        f.write(res.content)