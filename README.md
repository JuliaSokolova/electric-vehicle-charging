# electric-vehicle-charging 

This is a data exploratory project.
Using electric vehicle charging data, I want to to find out when drivers are likely to plug in their cars, and how much additional electricity demand that will create when the number of electric cars increases.
</br>
</br>

<p align="center"><img width=80% src=https://www.westrafo.com/wp-content/uploads/2019/04/P1000525.jpg> 
  
  
## Background & Motivation

While electric cars are usually still higher in their initial cost than traditional gas-powered vehicles, the amount of money you save in fuel and maintenance over the vehicle's lifetime offsets the higher up-front cost. According to the [U.S. Department of Energy](https://www.energy.gov/eere/electricvehicles/saving-fuel-and-vehicle-costs), the cost of fueling an electric vehicle is already about half the cost of fueling a gas-powered car, with an electric eGallon costing $1.24 and a gallon of gas costing $2.64 on average.



Washington State has a population of 7.5 million. There are about 52,000 electric vehicles in Washington State right now. By 2045, that population will grow to at least 9 million, and the total number of vehicles will grow to at least 4 million [Forbes](https://www.forbes.com/sites/jamesconca/2020/02/27/can-electric-cars-rise-in-time-to-save-us-washington-state-says-yes/#128a898170cf)
Scaling 

This disruptive growth will require a serious development of electric charging infrustructure. Charging at scale will require new architectures and scheduling to avoid adverse effects on the electric grid while reducing capital and operating costs. 


## Data Sources

To understand the challenges of large-scale EV charging and develop smart scheduling algorithms, California Tech University. together with PowerFlex Systems, developed The Adaptive Charging Network.

The ACN currently has over 80 EV charging ports in a garage on the Caltech campus which share a power limit of 300 kWh (enough for 42 conventional ports). The system currently charges an average of 65 EVs a day and over the last 3 years it has delivered over 2.3 million miles worth of charge. Their dataset contains information about every single charging session from 3 different locations.

In my project, I user data from a research university located in Pasadena, CA, with 54 EVSEs in one campus garage. The site is open to the public but most usage is from faculty, staff and students.


## Data Pipeline

The ACN data was easily accessable via [API](https://ev.caltech.edu/dataset). I uploaded and modified a file with over 28K datapoints in Spark dataframe, to move it from mulytlined .json file in two .csv tables that contain information about charging sessions and cars. I then used Pandas to explore data further. 

## Data Analysis

My first goal was to explore the patterns of car arriving at the charging station. 
I expected to see difference in the number of charging sessions for different month, weekdays and time of the day. Quick EDA proved my assumption:
  
<p align="center"><img width=100% src=https://github.com/JuliaSokolova/electric-vehicle-charging/blob/master/images/charging_sessions_per_weeday.png>  
  
No surprise the garage has more cars arriving during weekdays - it is mostly used by univesity staff and students.
At the monthly scale, there is also fluctuation. 

<p align="center"><img width=100% src=https://github.com/JuliaSokolova/electric-vehicle-charging/blob/master/images/charging_sessions_per_month.png> 
  
To  explore power demand fluctuation further, I looked into numbers of cars arriving at charging station for each hour of the day. I used  maximum likelihood estimation, assuming that my random variable 'number of cars arriving' has geometric distribution.




