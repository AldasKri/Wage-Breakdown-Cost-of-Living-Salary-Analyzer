import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np


st.set_page_config(
	page_title = 'Wage Breakdown',
	layout = 'wide'
)
st.title('Wage Breakdown')
st.write('If you are thinking of getting a job in a new city, use this app to speculate your new cost of living.')
st.write("Input all of the relevant information")
st.write('Disclaimer: This site should not be used to calculate your taxes, I am not an accountant or a financial planner.')

cities = {
    "New York, New York",
    "Los Angeles, California",
    "Chicago, Illinois",
    "Houston, Texas",
    "Phoenix, Arizona",
    "Philadelphia, Pennsylvania",
    "San Antonio, Texas",
    "San Diego, California",
    "Dallas, Texas",
    "San Jose, California",
    "Austin, Texas",
    "Jacksonville, Florida",
    "Fort Worth, Texas",
    "Columbus, Ohio",
    "Indianapolis, Indiana",
    "Charlotte, North Carolina",
    "San Francisco, California",
    "Seattle, Washington",
    "Denver, Colorado",
    "Nashville, Tennessee",
    "Oklahoma City, Oklahoma",
    "El Paso, Texas",
    "Washington, District of Columbia",
    "Boston, Massachusetts",
    "Portland, Oregon",
    "Las Vegas, Nevada",
    "Detroit, Michigan",
    "Memphis, Tennessee",
    "Louisville, Kentucky",
    "Baltimore, Maryland",
    "Milwaukee, Wisconsin",
    "Albuquerque, New Mexico",
    "Fresno, California",
    "Tucson, Arizona",
    "Sacramento, California",
    "Kansas City, Missouri",
    "Mesa, Arizona",
    "Atlanta, Georgia",
    "Omaha, Nebraska",
    "Colorado Springs, Colorado",
    "Raleigh, North Carolina",
    "Long Beach, California",
    "Virginia Beach, Virginia",
    "Miami, Florida",
    "Oakland, California",
    "Minneapolis, Minnesota"
}

city_utilities = {
    "New York, New York": 375,
    "Los Angeles, California": 375,
    "Chicago, Illinois": 450,
    "Houston, Texas": 350,
    "Phoenix, Arizona": 350,
    "Philadelphia, Pennsylvania": 450,
    "San Antonio, Texas": 350,
    "San Diego, California": 375,
    "Dallas, Texas": 350,
    "San Jose, California": 400,
    "Austin, Texas": 350,
    "Jacksonville, Florida": 350,
    "Fort Worth, Texas": 350,
    "Columbus, Ohio": 350,
    "Indianapolis, Indiana": 350,
    "Charlotte, North Carolina": 350,
    "San Francisco, California": 425,
    "Seattle, Washington": 450,
    "Denver, Colorado": 350,
    "Nashville, Tennessee": 350,
    "Oklahoma City, Oklahoma": 350,
    "El Paso, Texas": 350,
    "Washington, District of Columbia": 450,
    "Boston, Massachusetts": 450,
    "Portland, Oregon": 350,
    "Las Vegas, Nevada": 350,
    "Detroit, Michigan": 350,
    "Memphis, Tennessee": 350,
    "Louisville, Kentucky": 350,
    "Baltimore, Maryland": 350,
    "Milwaukee, Wisconsin": 350,
    "Albuquerque, New Mexico": 350,
    "Fresno, California": 320,
    "Tucson, Arizona": 350,
    "Sacramento, California": 350,
    "Kansas City, Missouri": 350,
    "Mesa, Arizona": 350,
    "Atlanta, Georgia": 350,
    "Omaha, Nebraska": 350,
    "Colorado Springs, Colorado": 350,
    "Raleigh, North Carolina": 350,
    "Long Beach, California": 364,
    "Virginia Beach, Virginia": 350,
    "Miami, Florida": 350,
    "Oakland, California": 380,
    "Minneapolis, Minnesota": 350
}

average_gas_prices = {
    "Washington": 4.66,
    "California": 4.65,
    "Hawaii": 4.47,
    "Oregon": 4.29,
    "Nevada": 3.92,
    "Alaska": 3.90,
    "Arizona": 3.58,
    "Illinois": 3.44,
    "Utah": 3.38,
    "Pennsylvania": 3.32,
    "New York": 3.25,
    "Montana": 3.24,
    "Connecticut": 3.21,
    "Colorado": 3.21,
    "Michigan": 3.29,
    "District of Columbia": 3.26,
    "Minnesota": 3.00,
    "Missouri": 2.80,
    "Kansas": 2.89,
    "South Carolina": 2.87,
    "Alabama": 2.84,
    "Tennessee": 2.85,
    "North Carolina": 2.86,
    "Iowa": 2.86,
    "South Dakota": 2.80,
    "Mississippi": 2.70,
    "Oklahoma": 2.75,
    "Louisiana": 2.76,
    "Texas": 2.79,
    "Arkansas": 2.78,
    "Indiana": 3.09
}


state_tax_rates = {
    "New York": 0.06,
    "California": 0.09,
    "Illinois": 0.0495,
    "Texas": 0.0,
    "Arizona": 0.045,
    "Pennsylvania": 0.03,
    "Washington": 0.0,
    "Colorado": 0.0455,
    "Tennessee": 0.0,
    "Oklahoma": 0.05,
    "District of Columbia": 0.0895,  # combined with local, could be adjusted
    "Massachusetts": 0.05,
    "Oregon": 0.09,
    "Nevada": 0.0,
    "Michigan": 0.0425,
    "Kentucky": 0.05,
    "Maryland": 0.05,
    "Wisconsin": 0.05,
    "New Mexico": 0.05,
    "Missouri": 0.055,
    "Georgia": 0.0575,
    "Florida": 0.0,
    "Ohio": 0.03,
    "Indiana": 0.0323,
    "North Carolina": 0.0525,
    "Nebraska": 0.054,
    "Minnesota": 0.0775,
    "Virginia": 0.0575
}


city_tax_rates = {
    "New York": 0.03876,
    "Los Angeles": 0.0,
    "Chicago": 0.0,
    "Houston": 0.0,
    "Phoenix": 0.0,
    "Philadelphia": 0.0375,
    "San Antonio": 0.0,
    "San Diego": 0.0,
    "Dallas": 0.0,
    "San Jose": 0.0,
    "San Francisco": 0.0,
    "Seattle": 0.0,
    "Denver": 0.0,
    "Nashville": 0.0,
    "Oklahoma City": 0.0,
    "El Paso": 0.0,
    "Washington": 0.0,  # DC is already included in state
    "Boston": 0.0,
    "Portland": 0.0,
    "Las Vegas": 0.0,
    "Detroit": 0.024,
    "Memphis": 0.0,
    "Louisville": 0.022,
    "Baltimore": 0.032,
    "Milwaukee": 0.01,
    "Albuquerque": 0.0,
    "Fresno": 0.0,
    "Tucson": 0.0,
    "Sacramento": 0.0,
    "Kansas City": 0.01,
    "Mesa": 0.0,
    "Atlanta": 0.0,
    "Austin": 0.0,
    "Jacksonville": 0.0,
    "Fort Worth": 0.0,
    "Columbus": 0.025,
    "Indianapolis": 0.0202,
    "Charlotte": 0.0,
    "Omaha": 0.015,
    "Colorado Springs": 0.0,
    "Raleigh": 0.0,
    "Long Beach": 0.0,
    "Virginia Beach": 0.0,
    "Miami": 0.0,
    "Oakland": 0.0,
    "Minneapolis": 0.015
}
rent_in_city = {
    "New York, New York": 2136,
    "Los Angeles, California": 1849,
    "Chicago, Illinois": 1523,
    "Houston, Texas": 1136,
    "Phoenix, Arizona": 1166,
    "Philadelphia, Pennsylvania": 1271,
    "San Antonio, Texas": 1036,
    "San Diego, California": 1938,
    "Dallas, Texas": 1354,
    "San Jose, California": 2331,
    "Austin, Texas": 1501,
    "Jacksonville, Florida": 1127,
    "Fort Worth, Texas": 1172,
    "Columbus, Ohio": 1089,
    "Indianapolis, Indiana": 1049,
    "Charlotte, North Carolina": 1317,
    "San Francisco, California": 2645,
    "Seattle, Washington": 1976,
    "Denver, Colorado": 1537,
    "Nashville, Tennessee": 1258,
    "Oklahoma City, Oklahoma": 895,
    "El Paso, Texas": 854,
    "Washington, District of Columbia": 2096,
    "Boston, Massachusetts": 2213,
    "Portland, Oregon": 1387,
    "Las Vegas, Nevada": 1100,
    "Detroit, Michigan": 759,
    "Memphis, Tennessee": 905,
    "Louisville, Kentucky": 915,
    "Baltimore, Maryland": 1189,
    "Milwaukee, Wisconsin": 939,
    "Albuquerque, New Mexico": 963,
    "Fresno, California": 1050,
    "Tucson, Arizona": 908,
    "Sacramento, California": 1347,
    "Kansas City, Missouri": 1115,
    "Mesa, Arizona": 1210,
    "Atlanta, Georgia": 1532,
    "Omaha, Nebraska": 1193,
    "Colorado Springs, Colorado": 1201,
    "Raleigh, North Carolina": 1259,
    "Long Beach, California": 1552,
    "Virginia Beach, Virginia": 1394,
    "Miami, Florida": 1575,
    "Oakland, California": 1850,
    "Minneapolis, Minnesota": 1214
}




def taxes(taxable_income,place, city_tax_rates, state_tax_rates):
	
	#Federal Taxes
	taxable_income -= 14600
	FICA = taxable_income*0.0765
	taxable_income -= FICA	
	total_federal = 0
	if taxable_income < 11001:
		total_federal = taxable_income*.1
	elif taxable_income <44726:
		total_federal = 11000*.1
		total_federal = total_federal + (taxable_income-11000)*.12
	elif taxable_income <95375:
		total_federal = (11000*.1)+((44725-11000)*.12)
		total_federal = total_federal+(taxable_income-44725)*.22
	else:
		total_federal = (11000*.1)+((44725-11000)*.12)+((95375-44725)*.22)
		total_federal += (taxable_income-44725)*.24
	taxable_income -= total_federal
	

	state_taxes = 0
	city_taxes = 0
	if place:
		#State Taxes
		state = place.split(',')[1]
		state = state.strip()
		state_taxes = state_tax_rates[state]*taxable_income
		taxable_income -= state_taxes	
				

		#City Taxes
		city = place.split(',')[0]
		city_taxes = city_tax_rates[city]*taxable_income
		
		return taxable_income, FICA, total_federal,state_taxes, city_taxes


col1, col2 = st.columns(2)
with col1:
	salary = st.slider("Salary: ", 0,150000,step = 500, key = "salary_slider")
	city = st.selectbox("Select a city: ",cities, index = None, placeholder = "Select the city")
	if city:
		city_name = city.split(',')[0]
		state_name = city.split(',')[1]
		state_name = state_name.strip()
	
	
	cola, colb = st.columns(2)
	with cola:
		IRA_per = st.number_input("401k percentage: ",min_value = 0.0,max_value = 10.0, step = 0.5, key = "IRA")
		IRA = salary*(IRA_per*.01)
		taxable_income = salary - IRA
		
		gas = st.slider(f'Gas per year: ', min_value = 0, max_value = 8000, value = 3*350, key = 'gas')	
		if city:
			st.write(f'Average price per gallon in {state_name} is {average_gas_prices[state_name]}')
	with colb:
		food = st.slider("Food Cost (Include Doordash, restaurants, etc): ", 0, 12000, 4200, key = "food")
		other_costs = st.number_input("Include the sum of costs not included here: ", key = "other_costs")
	
	timeline = st.pills('Wage Breakdown Per',['Week','Month','Year'])	

	pressed = False
	if st.button('Calculate'):
		pressed = True	

with col2:
	if city and salary and pressed:
		city_name = city.split(',')[0]
		state_name = city.split(',')[1]
		state_name = state_name.strip()
		takehome, FICA, federaltx, statetx, citytx = taxes(salary, city, city_tax_rates, state_tax_rates)
		spending = takehome - gas - food - other_costs - (city_utilities[city]*12) - (rent_in_city[city]*12)
		#Pie Chart
		labels = [f'{city_name} Average Utilities','Spending',f'{city_name} Rent (studio)','FICA','Federal Taxes',f'{state_name} Taxes',f'{city_name} Taxes','IRA','Food','Other Costs' ]
		sizes = [(city_utilities[city]*12), round(spending,2), round(rent_in_city[city]*12,2), round(FICA,2), round(federaltx,2), round(statetx,2), round(citytx,2), round(IRA,2), round(food,2), other_costs]
		
		if timeline == 'Week':
			 sizes = [round(x/52,2) for x in sizes]
		elif timeline == 'Month':
			sizes = [round(x/12,2) for x in sizes]
		pie_chart = px.pie(values = sizes, names = labels, title = f'Wage Breakdown Per {timeline}')
		pie_chart.update_traces(textinfo = 'label+value') 
		st.plotly_chart(pie_chart)
		 




