

CREATE TABLE main_index AS 
SELECT * FROM toptier_index 
UNION 
SELECT * FROM midtier_index
UNION 
SELECT * FROM bottomtier_index
UNION 
SELECT * FROM onebed_index 
UNION 
SELECT * FROM twobed_index 
UNION 
SELECT * FROM threebed_index 
UNION 
SELECT * FROM fourbed_index
UNION 
SELECT * FROM fivebed_index
ORDER BY regionid; 

ALTER TABLE main_index
ADD PRIMARY KEY (regionid);