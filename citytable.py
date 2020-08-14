import pandas as pd
import execute
import tools 
import matplotlib.pyplot as plt 


filename = ("ZillowByCity.csv")

data = pd.read_csv(filename)
citycount = data['RegionID'].count()

ID = 6181

test = tools.clean(data, ID, 8)
print(test)


fig = test.plot()
plt.show()

fig1 = fig.get_figure()
fig1.savefig("yo.png")
