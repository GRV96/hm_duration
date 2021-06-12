from hm_duration import HM_Duration


ACTUAL_STR = "Actual: "
COLON = ":"
EXPECTED_STR = "Expected: "
PERIOD = "."


def hour_minute_str(hours, minutes):
	return str(hours) + COLON + str(minutes)


def print_actual_and_expected_durations(
		actual_h, actual_m, expected_h, expected_m):
	print(ACTUAL_STR + hour_minute_str(actual_h, actual_m))
	print(EXPECTED_STR + hour_minute_str(expected_h, expected_m))


def print_actual_and_expected_values(actual_value, expected_value):
	print(ACTUAL_STR + str(actual_value))
	print(EXPECTED_STR + str(expected_value))


def test_eq(h1, m1, h2, m2, expected_eq):
	d1 = HM_Duration(h1, m1)
	d2 = HM_Duration(h2, m2)
	actual_eq = d1 == d2

	try:
		assert actual_eq == expected_eq
	except AssertionError:
		print("Equality test failed for "
			+ str(d1) + " and " + str(d2) + PERIOD)
		print_actual_and_expected_values(actual_eq, expected_eq)
		print()


def test_instantiation(hours, minutes, expected_h, expected_m):
	duration = HM_Duration(hours, minutes)
	actual_h = duration.hours
	actual_m = duration.minutes

	try:
		assert actual_h == expected_h and actual_m == expected_m
	except AssertionError:
		print("Instantiation test failed for "
			+ hour_minute_str(hours, minutes) + PERIOD)
		print_actual_and_expected_durations(
			actual_h, actual_m, expected_h, expected_m)
		print()


def test_to_hours(hour_arg, minute_arg, expected_h_num):
	duration = HM_Duration(hour_arg, minute_arg)
	actual_h_num = duration.to_hours()

	try:
		assert actual_h_num == expected_h_num
	except AssertionError:
		print("Conversion to hours test failed for "
			+ hour_minute_str(hour_arg, minute_arg) + PERIOD)
		print_actual_and_expected_values(actual_h_num, expected_h_num)
		print()


def test_to_minutes(hour_arg, minute_arg, expected_m_num):
	duration = HM_Duration(hour_arg, minute_arg)
	actual_m_num = duration.to_minutes()

	try:
		assert actual_m_num == expected_m_num
	except AssertionError:
		print("Conversion to minutes test failed for "
			+ hour_minute_str(hour_arg, minute_arg) + PERIOD)
		print_actual_and_expected_values(actual_m_num, expected_m_num)
		print()


test_instantiation(0, 0, 0, 0) # 00:00
test_instantiation(0, 7, 0, 7) # 00:07
test_instantiation(7, 0, 7, 0) # 07:00
test_instantiation(7, 7, 7, 7) # 07:07

test_instantiation(0, 77, 1, 17) # 00:77
test_instantiation(7, 77, 8, 17) # 07:77

test_eq(0, 0, 0, 0, True) # 00:00 == 00:00
test_eq(0, 7, 0, 7, True) # 00:07 == 00:07
test_eq(7, 1, 7, 0, False) # 07:01 != 07:00
test_eq(8, 7, 7, 7, False) # 08:07 != 07:07

test_to_hours(0, 0, 0.0)
test_to_hours(0, 15, 0.25)
test_to_hours(0, 17, 0.28333333333333333333333333333333)
test_to_hours(2, 0, 2.0)
test_to_hours(2, 30, 2.50)

test_to_minutes(0, 0, 0)
test_to_minutes(0, 17, 17)
test_to_minutes(1, 17, 77)
test_to_minutes(2, 17, 137)
