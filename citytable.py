import pandas as pd
import execute
import tools 
import matplotlib.pyplot as plt 


filename = ("ZillowByCity.csv")

data = pd.read_csv(filename)
citycount = data['RegionID'].count()


RegionID = data['RegionID'][:5]



for ID in RegionID:
    city_to_db = tools.clean(data, ID, 8)
    tablequery = "CREATE TABLE %s (id INT AUTO_INCREMENT PRIMARY KEY, dt DATETIME NOT NULL, price INT)" %(ID)
    city_to_db.columns = ['price']
    # Change column name into "price"
    
    rowcount = len(city_to_db.index)
    total = ""
    for j in range(rowcount):
        if (j != (rowcount-1)):
                entry = "('%s',%s)," %(city_to_db.index[j], city_to_db['price'][j])
        else:
                entry = "('%s',%s)" %(city_to_db.index[j], city_to_db['price'][j])
        total = total + entry
    print(total)


# fig = test.plot()
# plt.show()

# fig1 = fig.get_figure()
# fig1.savefig("yo.png")
