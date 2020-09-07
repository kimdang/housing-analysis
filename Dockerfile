from python:3.7 
RUN pip3 install pymysql mysqlclient==1.4.6 Django
RUN pip3 install pandas 
RUN pip3 install matplotlib
RUN pip3 install seaborn
RUN pip3 install -U numpy scipy scikit-learn

