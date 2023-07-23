def calculate(first_int, second_int, operator):
	try:
		if operator == "+":
			result = first_int + second_int
		elif operator == "-":
			result = first_int - second_int
		elif operator == "*":
			result = first_int * second_int
		elif operator == "/":
			result = first_int / second_int
	except ZeroDivisionError:
	    result = "Unable to divide 0s"
	return(result)