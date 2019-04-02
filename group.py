import itertools
import statistics
from random import shuffle

NUM_PERSONS = 13

class Person:

	def __init__(self, person_name):
		self.name = person_name
		self.meetings = [0] * NUM_PERSONS
		
	def __str__(self):
		return self.name
		
	__repr__ = __str__

"""
Print the different groups for num_iter number of times

:list_of_persons An array of person names in the group
:num_iters An integer number of group splits to produce
:split An array indicating the way the groups are sploit
"""
def print_groups(list_of_persons, num_iters, split):	
	shuffle(list_of_persons)
	for i in range(num_iters):
		print ("Groups " + str(i+1)) + ":\n"
		combos = find_all_combos(range(len(list_of_persons)), split)
		min_val = 2 * num_iters * len(list_of_persons) # Somewhat arbitrary high number
		best_groups = []
		for group in combos: #e.g. one example group is [[1,2,3,4],[5,6],[7,8,9]]
			val = 0
			for inner_group in group: # e.g. [1,2,3,4]
				inter_group_combos = itertools.combinations(inner_group, 2)
				for combo in inter_group_combos:
					val += list_of_persons[combo[0]].meetings[combo[1]]
			if val < min_val:
				best_groups = [group]
				min_val = val
			elif val == min_val:
				best_groups.append(group)
		best_group = select_group_with_balanced_meeting_numbers(list_of_persons, best_groups)
		add_meeting_values_for_group(list_of_persons, best_group)
		print_meetings_formatted(list_of_persons, best_group)

def select_group_with_balanced_meeting_numbers(list_of_persons, groups):
	min_std_val = len(list_of_persons) # Somewhat arbitrary high number
	meetings_per_person = [0] * len(list_of_persons)
	best_group = []
	for i in range(len(list_of_persons)):
		meetings_per_person[i] += sum(list_of_persons[i].meetings)
	for group in groups:
		new_meetings_per_person = list(meetings_per_person)
		for inner_group in group: # e.g. [1,2,3,4]
			inter_group_combos = itertools.combinations(inner_group, 2)
			for combo in inter_group_combos:
				new_meetings_per_person[combo[0]] += 1
				new_meetings_per_person[combo[1]] += 1
		std_val = statistics.stdev(new_meetings_per_person)
		if std_val < min_std_val:
			best_group = group
			min_std_val = std_val
	return best_group
		
def add_meeting_values_for_group(list_of_persons, group):
	for inner_group in group: # e.g. [1,2,3,4]
		inter_group_combos = itertools.combinations(inner_group, 2)
		for combo in inter_group_combos:
			list_of_persons[combo[0]].meetings[combo[1]] += 1
			list_of_persons[combo[1]].meetings[combo[0]] += 1

# Helper print function to print a list of persons
def print_person_meetings_matrix(list_of_persons):
	for person in list_of_persons:
		print (person.meetings)

#  Helper print function to correspond person indices to their names
def print_meetings_formatted(list_of_persons, groups):
	group_num = 1
	for group in groups: # e.g. [1,2,3]
		print ("Group " + str(group_num) + ": ")
		for index in group:
			print (list_of_persons[index].name + " ")
		print ("\n")
		group_num += 1

def find_all_combos(arr, split):
	total = 0
	for split_entry in split:
		total += split_entry
	if total != len(arr):
		print("The split doesn't add up!")
		return []
	split.sort(reverse=True)
	return find_all_combos_helper(arr, split)

# Assume all elements are unique
def find_all_combos_helper(arr, split):
	if (len(split) == 1):
		return [[arr]]
	result = []
	if (split[0] == split[1]): # Need to avoid duplicates
		# Arbitrarily choose the first one
		combos = itertools.combinations(range(len(arr)-1), split[0]-1) # Choose which INDICES we want to keep
		# Append the combos
		for combo in combos:
			remaining_arr = list(arr[1:])
			arr_chosen = [arr[0]]
			for index in combo: # Index <= len(arr)-2
				arr_item = arr[index+1]
				arr_chosen.append(arr_item)
				remaining_arr.remove(arr_item)
			remaining_combos = find_all_combos_helper(remaining_arr, split[1:])
			for remaining_combo in remaining_combos:
				result.append([arr_chosen]+ remaining_combo)
	else:
		combos = itertools.combinations(range(len(arr)), split[0]) # Choose which INDICES we want to keep
		# Append the combos
		for combo in combos:
			remaining_arr = list(arr)
			arr_chosen = []
			for index in combo:
				arr_item = arr[index]
				arr_chosen.append(arr_item)
				remaining_arr.remove(arr_item)
			remaining_combos = find_all_combos_helper(remaining_arr, split[1:])
			for remaining_combo in remaining_combos:
				result.append([arr_chosen] + remaining_combo)
	return result
			
def main():
	# The following for sample purposes.
	list_of_people = []
	list_of_people.append(Person("Alex"))
	list_of_people.append(Person("Chris"))
	list_of_people.append(Person("David"))
	list_of_people.append(Person("Harry"))
	list_of_people.append(Person("Heewon"))
	list_of_people.append(Person("Iris"))
	list_of_people.append(Person("Janice"))
	list_of_people.append(Person("Kevin"))	
	list_of_people.append(Person("Kuo"))	
	list_of_people.append(Person("Monica"))
	list_of_people.append(Person("Ray"))	
	list_of_people.append(Person("Ren-Jay"))
	list_of_people.append(Person("Richy"))
	print_groups(list_of_people, 7, [4,5,4])

if __name__ == "__main__":
	main()
	
	
