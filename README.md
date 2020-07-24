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
  
### Bayasian method to model user's behavior

I used Bayasian statistics to infer behaviour of cars arriving model, looking into a question if the user's charging habits have changed over time, either gradually or suddenly. To do so, I looked into time persiod starting Jan, 1 2020.

Using PyMC3 library (Markov Chain Monte Carlo), I generated random variables from the posterior distributions of λ1,λ2 and τ. The images below show what the posterior distributions look like.

<p align="center"><img width=100% src=https://github.com/JuliaSokolova/electric-vehicle-charging/blob/master/images/posteriour_probabilities.png> 

<p align="center"><img width=100% src=https://github.com/JuliaSokolova/electric-vehicle-charging/blob/master/images/posteriors_tau.png> 

The model showes λ1 around 27 and λ2 is around 2. The posterior distributions of the two λs are clearly distinct, indicating that it is indeed likely that there was a change in the user's charging behaviour. The posterior distribution for τ showes a 65% chance that the user's behaviour changed on day 73 (May 13, 2020), which corrspond to California 'stay-at-home' order due to COVID19.

As expected, my analysis shows strong support for believing the user's behavior did change (λ1 would have been close in value to λ2 had this not been true), and that the change was sudden rather than gradual (as demonstrated by τ's strongly peaked posterior distribution). 

<p align="center"><img width=100% src=https://github.com/JuliaSokolova/electric-vehicle-charging/blob/master/images/expected_number_of_cars_arrive.png> 


### Maximum likelihood estimation for car arrivals by the time of day

To  explore power demand fluctuation further, I looked into numbers of cars arriving at charging station for each hour of the day. I used  maximum likelihood estimation, assuming that my random variable 'number of cars arriving' has geometric distribution. 
Data show that at peak we could expect up to 8 cars arriving every hour between 3 and 5 PM; all other time, cars arrive at an average rate betwen 2 and 4 cars per hour. 

<p align="center"><img width=100% src=https://github.com/JuliaSokolova/electric-vehicle-charging/blob/master/images/cars_by_the_hour_max_likelihood.png> 

 
### Additional data to estimate the demand of electricity

To predict electricity demand, we would also need to know how much kWh our users would request. For that, I looked into average charge requests for one car, distributed by the hour of arrival.
It turns out, the users who arrive in the mornings, betwen 6 AM and noon, demand the highest amount of electricity, between 30 and 40 kWh. For cars arriving at other times, the the number stays around 20 kWh.

<p align="center"><img width=100% src=https://github.com/JuliaSokolova/electric-vehicle-charging/blob/master/images/charge_request_by_hour.png>


It also worth to look into the lengths of charging sessions. Below is the graph of average lengths of one charging session, distributed by the time of car's arrival. 

<p align="center"><img width=100% src=https://github.com/JuliaSokolova/electric-vehicle-charging/blob/master/images/charge_request_by_hour.png>

### Hypothesis testing: Welch t-test 

From a graph we can see there is a visible fluctiuaton of this random variable. 
To prove my hypothesis "the average length of a charging session is different for daytime (8AM - 10PM) and nighttime (10PM - 8AM)", I run Welch t-test on two corresponding datasets of sessions charging times.

The mean session length in day group was 3.24 hours (SD = 2.62), whereas the mean session length in night group was 2.47 (SD = 2.81). A Welch two-samples t-test showed that the difference was statistically significant, with t-statistic 19.51 and p < 0.0001.


###

