from .duration_string import duration_to_str
from math import floor


_MINS_IN_HOUR = 60
"""
The number of minutes in one hour
"""


class HM_Duration:
	"""
	This class represents durations as a number of hours and a number of
	minutes. It also allows to perform arithmetic operations on them.
	"""

	def __init__(self, hours, minutes):
		"""
		The constructor needs the number of hours and the number of minutes
		that make a duration.

		Args:
			hours (int): a number of hours
			minutes (int): a number of minutes

		Raises:
			ValueError: if hours and minutes do not have the same sign
		"""
		if hours * minutes < 0:
			raise ValueError(
				"Arguments hours and minutes must have the same sign.")

		if hours < 0 or minutes < 0:
			self._sign = -1
		else:
			self._sign = 1

		self._hours = abs(hours)
		self._minutes = abs(minutes)
		self._regularize()

	def __add__(self, other):
		"""
		Creates an instance that represents the sum of self and other.

		Args:
			other (HM_Duration): another duration

		Returns:
			HM_Duration: the sum of self and other
		"""
		sum_as_mins = self.to_minutes() + other.to_minutes()
		return HM_Duration(0, sum_as_mins)

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False

		return self._hours == other._hours\
			and self._minutes == other._minutes

	def __mul__(self, number):
		"""
		Creates an instance that represents the product of self by a number.
		The result is approximated to the nearest minute.

		Args:
			number (int or float): any integral or real number

		Returns:
			HM_Duration: the product of self by a number
		"""
		prod_as_mins = int(_round_half_up(self.to_minutes() * number))
		return HM_Duration(0, prod_as_mins)

	def __rmul__(self, number):
		return self.__mul__(number)

	def __repr__(self):
		return self.__class__.__name__ +\
			"(" + str(self.hours) + ", " + str(self.minutes) + ")"

	def __str__(self):
		return duration_to_str(self.hours, self.minutes)

	def __sub__(self, other):
		"""
		Creates an instance that represents the difference of self and other.

		Args:
			other (HM_Duration): another duration

		Returns:
			HM_Duration: the difference of self and other
		"""
		diff_as_mins = self.to_minutes() - other.to_minutes()
		return HM_Duration(0, diff_as_mins)

	def __truediv__(self, number):
		"""
		Creates an instance that represents the quotient of self by a number.
		The result is approximated to the nearest minute.

		Args:
			number (int or float): any integral or real number

		Returns:
			HM_Duration: the quotient of self by a number
		"""
		quo_as_mins = int(_round_half_up(self.to_minutes() / number))
		return HM_Duration(0, quo_as_mins)

	@property
	def hours(self):
		"""
		This read-only property returns this duration's number of hours.
		"""
		return self._sign * self._hours

	@property
	def minutes(self):
		"""
		This read-only property returns this duration's number of minutes.
		"""
		return self._sign * self._minutes

	def _regularize(self):
		"""
		Makes sure that the number of minutes is less than 60.
		"""
		self._hours += self._minutes // _MINS_IN_HOUR
		self._minutes = self._minutes % _MINS_IN_HOUR

	def to_hours(self):
		"""
		Converts this duration to a real number of hours.

		Returns:
			float: a real number of hours equal to this duration
		"""
		num_of_hours = self._hours + self._minutes / _MINS_IN_HOUR
		return self._sign * num_of_hours

	def to_minutes(self):
		"""
		Converts this duration to an integral number of minutes.

		Returns:
			int: an integral number of minutes equal to this duration
		"""
		num_of_minutes = self._hours * _MINS_IN_HOUR + self._minutes
		return self._sign * num_of_minutes


def _round_half_up(n, decimals=0):
	# Source: https://realpython.com/python-rounding/#rounding-half-up
    multiplier = 10 ** decimals
    return floor(n*multiplier + 0.5) / multiplier