"""
Day 1 : Data Analysis (Pesa pulse)

APPROACH
I used Python library to fetch 10 customer records from the JSON placeholder users API, I explored the nested JSON structure, extracted 12 fields per customer used loops and dictionary comprehensions to analyze customers by city and email domain. 
I then created pandas DataFrame, esported two csv files and generated two charts in the output folder.

KEY FINDINGS
1. Customer disrtibution -> There were no geographical concentration in this sample since the 10 customers came from different cities therefore more data is needed to identify more potential marketing targets.
2. Email domains -> The biz suffix appeared most times i.e 3 out of 10 (30%). this shows a difference in domain distribution although more data would be needed  to establish a meaningful business trend.
3. Data quality -> Latitude and longitude were returned as text, so i converted them to floatind-piont numbers for easier numeral analysis. 

ASSUMTION AND LIMITATION
-Email domain were classified using the text after the last dot.
-If  the API request fails, the program displays an error and continues with an   empty   dataset.
-Since the sample contains only 10 customers, the findings should not be generalised to the wider population.