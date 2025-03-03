import sys
import os 
import numpy as np

class file_handler:
	"""
	Public methods:

	__init__
	file_iteration
	data_conversion
	runtime 

	Class to get data from the SIMS output files. 
	The data is collected in groups by the delimiters in the data file, e.g. **** DATA START*** contains all numerical data. 
	Operations are then preformed to convert the data to human and machine readable formats. 

	The class can easily be changed to take an arbitrary data file with a known delimiter between types of parameters. 
	If there are several data sets, submit a list with strings denoting the start of the dataset and the corresponding
	attribute of the class will be a dictionary with the denoted rows as keys with substance as the first element
	and the x and y axis as the second and third element.  
	
	The class is initialized with the plotting module, if you wish to only use the file decoding aspect please view the sample 
	running in the docstring of the runtime method.
	"""

	def __init__(self, filename):
		"""Gets the filename from which the data is collected. """
		self.filename = filename 

	def file_iteration(self, delim = "***"):
		"""
		Walks through the supplied data file and stores all lines in string format. The data is saved
		by assigning each set of rows to the corresponding delimiter. The delimiting value (by default \" *** \")
		determines where the method separates the objects. Each part of the file can be accessed through 

		getattr(ClassInstance, File Partition)

		where File Partition is the string directly following the delimiter. 

		Method will be expanded to be more robust in taking delimiters with spaces adjacent to the string following the 
		delimiter. 

		"""

		num_lines = sum(1 for line in open(self.filename))

		
		#full_file_path = self.file_location()
		with open(self.filename) as self.file_object:
			line_indices = np.arange(0, num_lines, 1, dtype = int)

			data_type_indices = []
			lines = []

			for line, i in zip(self.file_object, line_indices):
				decoded = " ".join(line.split())
				lines.append(decoded)
				if line[:3] == delim:
					data_type_indices.append(i)

			self.attribute_names = []


			for index_of_data_type, i in zip(data_type_indices, np.arange(0, len(data_type_indices)-1, 1,  dtype = int)): 
				self.attribute_names.append(str(lines[index_of_data_type][4:-4]))
				setattr(self, str(lines[index_of_data_type][4:-4]), lines[index_of_data_type + 1: data_type_indices[i + 1 ] - 1]) 
			
		
	def data_conversion(self, data_name = "DATA START", key_row= [2, 3]):
		"""
		Strictly needs to be run after the file_iteration method.
		Formats the strings contained in the data_name attribute of the class to float.

		Keyword arguments:
		data_name (string) = string following delimiter before the data set.
		key_row (list) = list with the rows in the data set which contains information about the data

		returns list of datasets where each dictionary has the keys:

		data = 2 x n nested list where data[0] contains all data points corresponding to the key \" x_unit \"
		x_unit = string with physical unit of data[0]
		y_unit = string with physical unit of data[1]
		sample info = nested list containing sample id, original filename, sample code etc.
		sample name = name of the element measured by the SIMS process  
		"""
		try:
			data_set = getattr(self, data_name)
		except:
			raise TypeError("No attribute of class with name %s. Check that there are no extra spaces in variable name.") %data_name

		self.substances = data_set[key_row[0]].split(" ")
		units = data_set[key_row[1]].split(" ")

		x = []
		for line in data_set[key_row[1] + 1:] :
			dat = line.split(" ")
			a = [float(c) for c in dat]
			x.append(a)

		reshaping = np.shape(x)
		u = np.reshape(x, (reshaping[0], reshaping[1]))
	
		variables_per_substance = len(x[0])/len(self.substances)

		self.list_of_datasets = []

		for name, number in zip(self.substances, np.arange(0, len(x[0]), 2, dtype = int)):
			y = {}
			if variables_per_substance == 2 and x[0][0] != 0 :
				units = [x for x in units if x != "Time"]

			y["data"] = [u[:,number], u[:,number + 1]]
			y["x_unit"] = units[number]
			y["y_unit"] = units[number + 1]
			y["sample info"] = getattr(self, "DATA FILES")
			y["sample element"] = name

			setattr(self, name, y)
			self.list_of_datasets.append(getattr(self, name))

		return self.list_of_datasets

	def runtime(self, delim = "***", data_name = "DATA START", key_row= [2, 3]):
		"""
		Runs the file iterator and data conversion and returns a touple of the names of the analyzed elements 
		and dictionaries containing all data 
		"""

		self.file_iteration(delim)
		x = self.data_conversion(data_name, key_row)

		return (self.substances, x)



