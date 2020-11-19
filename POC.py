expected_start_position_for_standard_bicep_curl = (0, 1, 0)
expected_sample_positions_for_one_standard_bicep_curl = [expected_start_position_for_standard_bicep_curl]
def generate_expected_sample_points(count, dv):
	global expected_sample_positions_for_one_standard_bicep_curl
	final_index = len(expected_sample_positions_for_one_standard_bicep_curl) - 1
	for i in range(final_index, final_index + count):
		x = expected_sample_positions_for_one_standard_bicep_curl[i][0]
		y = expected_sample_positions_for_one_standard_bicep_curl[i][1]
		z = expected_sample_positions_for_one_standard_bicep_curl[i][2]
		dx = dv[0]
		dy = dv[1]
		dz = dv[2]
		xf = round(x + dx, 1)
		yf = round(y + dy, 1)
		zf = round(z + dz, 1)
		expected_sample_positions_for_one_standard_bicep_curl.append((xf, yf, zf))
generate_expected_sample_points(10, (0, -0.1, -0.1)) # 0 deg -> 90 deg
generate_expected_sample_points(8, (0, -0.1, 0.1)) # 90 deg -> 160 deg
generate_expected_sample_points(8, (0, 0.1, -0.1)) # 160 deg -> 90 deg
generate_expected_sample_points(10, (0, 0.1, 0.1)) # 90 deg -> 0 deg



class Forearm:
	def __init__(self, start_position):
		self.position = start_position
	def tilt_left(self, magnitude):
		self.position = (
			-magnitude,
			self.position[1],
			self.position[2]
		)
	def tilt_right(self, magnitude):
		self.position = (
			magnitude,
			self.position[1],
			self.position[2]
		)
	def reposition(self, position):
		self.position = position
user_forearm = Forearm(expected_start_position_for_standard_bicep_curl)

index_of_expected_sample = 0
acceptable_deviation = 0.05


def later_index_if_matches():
	global expected_sample_positions_for_one_standard_bicep_curl, index_of_expected_sample, acceptable_deviation, user_forearm

	user_position = user_forearm.position
	user_x = user_position[0]
	user_y = user_position[1]
	user_z = user_position[2]

	count = 0
	for sample in expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample:]:
		expected_x = sample[0]
		expected_y = sample[1]
		expected_z = sample[2]

		dx = user_x - expected_x
		dy = user_y - expected_y
		dz = user_z - expected_z
		if abs(dx) < acceptable_deviation and abs(dy) < acceptable_deviation and abs(dz) < acceptable_deviation:
			return index_of_expected_sample + count
		count += 1
	return index_of_expected_sample

def earlier_index_if_matches():
	global expected_sample_positions_for_one_standard_bicep_curl, index_of_expected_sample, acceptable_deviation, user_forearm

	user_position = user_forearm.position
	user_x = user_position[0]
	user_y = user_position[1]
	user_z = user_position[2]

	count = 0
	for i in reversed(range(0, index_of_expected_sample)):
		sample = expected_sample_positions_for_one_standard_bicep_curl[i]
		expected_x = sample[0]
		expected_y = sample[1]
		expected_z = sample[2]

		dx = user_x - expected_x
		dy = user_y - expected_y
		dz = user_z - expected_z
		if abs(dx) < acceptable_deviation and abs(dy) < acceptable_deviation and abs(dz) < acceptable_deviation:
			return index_of_expected_sample - count
		count += 1
	return index_of_expected_sample

def feedback_for_incorrect_form(ux, uy, uz, ex, ey, ez, bx, by, bz):
	global expected_sample_positions_for_one_standard_bicep_curl, index_of_expected_sample, acceptable_deviation, user_forearm

	feedback = ""

	offset = earlier_index_if_matches() - index_of_expected_sample
	if offset < 0:
		 feedback += "[pacing] the user changed curling direction too early!\n"
	else:
		offset = later_index_if_matches() - index_of_expected_sample
		if offset > 0:
			feedback += "[pacing] the user is curling too fast!\n"
		else:
			feedback += "[pacing] the user is on pace\n"

	if not bx:
		feedback += "[motion] the user's arm is tilted too much to the "
		if ux < ex:
			feedback += "left"	
		else:
			feedback += "right"
		feedback += "!\n"	
	if not by or not bz:
		feedback += "[motion] the user is "
		if uy < ey or uz < ez:
			feedback += "curling up"
		else:
			feedback += "curling down"
		feedback += "!\n"
	return (offset, feedback)

def feedback():
	global expected_sample_positions_for_one_standard_bicep_curl, index_of_expected_sample, acceptable_deviation, user_forearm

	user_position = user_forearm.position
	user_x = user_position[0]
	user_y = user_position[1]
	user_z = user_position[2]

	expected_position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample]
	expected_x = expected_position[0]
	expected_y = expected_position[1]
	expected_z = expected_position[2]

	dx = user_x - expected_x
	dy = user_y - expected_y
	dz = user_z - expected_z

	x_is_acceptable = abs(dx) < acceptable_deviation
	y_is_acceptable = abs(dy) < acceptable_deviation
	z_is_acceptable = abs(dz) < acceptable_deviation

	if x_is_acceptable and y_is_acceptable and z_is_acceptable:
		return (1, "[pacing][motion] The user's form is acceptable")
	else:
		return feedback_for_incorrect_form(user_x, user_y, user_z, expected_x, expected_y, expected_z, x_is_acceptable, y_is_acceptable, z_is_acceptable)

print("Press the Enter/Return key to continue the program when it pauses (like right now!).")
input()
print()
print("This program simulates a way user feedback could be determined by FitForm.")
print()
print("Data sampled from sensors is simulated, however the system response is computed as it would be.")
print()
print("We will be simulating a user attempting to do a standard bicep curl with one arm. A play-by-play follows...")
input()



print()
print()
print("USER: Arm is at rest by their side, forearm facing out with dumbell being held")
print()
result = feedback()
print("SYSTEM:")
print(result[1])
index_of_expected_sample += result[0]
input()



print()
print()
print("USER: Curls up too fast")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample + 5]
result = feedback()
print("SYSTEM:")
print(result[1])
index_of_expected_sample += result[0]
input()



print()
print()
print("USER: Begins curling in the opposite direction without completing the curl")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample - 2]
result = feedback()
print("SYSTEM:")
print(result[1])
index_of_expected_sample += result[0]
index_of_expected_sample += 1
index_of_expected_sample = later_index_if_matches()
input()

print()
print()
print("USER: Immediately after the previous event")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample]
result = feedback()
print("SYSTEM:")
print(result[1])
print("(here the system calibrated to the user's position, so they can continue their exercise, even though they made a mistake)")
input()


print()
print()
print("USER: Curls down correctly")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample]
result = feedback()
print("SYSTEM:")
print(result[1])
input()

print()
print()
print("USER: Curls up before completing curl down")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample - 2]
result = feedback()
print("SYSTEM:")
print(result[1])
input()


print()
print()
print("USER: Immediately after the previous event")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample]
result = feedback()
print("SYSTEM:")
print(result[1])
print("(here the system calibrated to the user's position, so they can continue their exercise, even though they made a mistake)")
index_of_expected_sample += 1
input()



print()
print()
print("USER: Continues to curl up but tilts forearm left")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample]
user_forearm.tilt_left(0.1)
result = feedback()
print("SYSTEM:")
print(result[1])
index_of_expected_sample += 1
input()



print()
print()
print("USER: Continues to curl up but tilts forearm right to correct it, but overshoots")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample]
user_forearm.tilt_right(0.2)
result = feedback()
print("SYSTEM:")
print(result[1])
index_of_expected_sample += 1
input()



print()
print()
print("USER: Continues to curl up and tilts forearm left to correct it")
print()
user_forearm.position = expected_sample_positions_for_one_standard_bicep_curl[index_of_expected_sample]
user_forearm.tilt_left(0)
result = feedback()
print("SYSTEM:")
print(result[1])
index_of_expected_sample += 1
input()
