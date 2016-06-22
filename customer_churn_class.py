#Allows a user to analyze their customers's churn over different time periods
__author__ = "Frederick Robson"
__email__ = "frederickwlrobson@gmail.com"

import csv;


class ChurnAnalysis:

	def __init__(self,file_name,churn_period = 1):
		self.churn_period = churn_period
		self.__data = self.__read_customer_data(file_name)
		self.absolute = self.__data[0]
		self.relative = self.__data[1]
		self.absolute_churn_dict = self.__calculate_churn_tp_dict(self.absolute,self.churn_period)
		self.relative_churn_dict = self.__calculate_churn_tp_dict(self.relative,self.churn_period)

	def __calculate_relative(self, revenue_list):
		"""
			Takes in a list of revenues and returns the relative start date
			@revenue_list: a list of revenue for each time period
			@return: the time period the subscription started
		"""
		count = 0 
		for time_period in revenue_list:
			if(time_period != 0): break
			count+=1
		return revenue_list[count:]

	def __csv_string_to_float(self, revenue_list_str):
		"""
			Converts the csv strings to floats
			@revenue_list_str: the list of revenue per time-period formatted as a string
			@return: the list of revenue per time period formatted as floats 
		"""
		revenue_list_flt = []
		for time_period in revenue_list_str:
			time_period = time_period.replace(',','')
			try:
				revenue_list_flt.append(float(time_period))
			# in case of error, set revenue in time period to 0
			except:
				 revenue_list_flt.append(0)
		return revenue_list_flt

	def __check_churned_in_tp(self, customer_revenue, tp, churn_period):
		"""
			Checks whether a customer churned in a particular time period
			@customer_revenue: the customer's revenue over different time periods
			@tp: The time period for which we are checkign whether the customer has churned
			@churn_period: How many time periods it takes a customer to churn
			@return: True if the customer did churn in that tp, else false
		"""
		for i in range(churn_period):
			#Ensures that you do not try to check whether a company has churned in the future
			if(tp + i >= len(customer_revenue)): return False
			tp_revenue = customer_revenue[tp + i]
			if(tp_revenue > 0): return False
		return True


	def __calculate_time_period_churned(self, customer_revenue, churn_period):
		"""
			Calculates the time_period in which a customer churned
			@customer: a list containing the customers revenue for different
			time periods
			@churn_period: the number of time periods required to churn
			@return: the time period churned in or null if customer did not churn

		"""
		started = False #Describing whether has begun to be a customer or not
		for tp in range(len(customer_revenue)):
			tp_revenue = customer_revenue[tp]
			if(tp_revenue > 0): started = True #indicates that the customer has actually started subscribing
			if(started and tp_revenue == 0): 
				if(self.__check_churned_in_tp(customer_revenue, tp, churn_period)):
					return tp #return the time period the customer churned if they did churn

		return None #return none if the customer didnt churn

	def __calculate_churn_tp_dict(self,relative_revenue, churn_period):
		"""
			Calculates the churn rate for customers in relative terms. 
			Aka calculated the number of customers who churn one month after joining,
			two months after joining etc
			@relative_revenue = Revenue by customer starting at first month of subscription
			@churn_period = the number of time periods required to churn
			@return: a dictionary contanining the time every customer churned. If the customer did not churn, None is recorded
			eg: {John Doe: 3} represents that customer John Doe churned in the 3rd time period after he started
		"""
		churned_time_period = {} #Dict containing the month that the customers churned
		for customer in relative_revenue:
			customer_revenue = relative_revenue[customer]
			time_period_churned = self.__calculate_time_period_churned(customer_revenue,churn_period)
			churned_time_period[customer] = time_period_churned
		return churned_time_period


	def __read_customer_data(self, filename):

		"""
			Reads a csv file containing customer data
			File should be formatted
			@filename: The name of the file to be read
			@return: Tuple containing absolute, relative  
		"""
		absolute_time_period = {}
		relative_time_period = {}
		with open(filename) as csvfile:
			fileReader = csv.reader(csvfile, delimiter = ',')
			for row in fileReader:
				customer = row[0]
				if(type(customer) != str): print customer
				revenue = self.__csv_string_to_float(row[1:])
				absolute_time_period[customer] = revenue
				relative_time_period[customer] = self.__calculate_relative(revenue)
		csvfile.close
		return (absolute_time_period, relative_time_period)





