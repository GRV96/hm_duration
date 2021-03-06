from .duration_string import duration_from_str, duration_to_str
from math import floor


_MINS_IN_HOUR = 60
"""
The number of minutes in one hour
"""


class HM_Duration:
	"""
	This class represents durations as a number of hours and a number of
	minutes. Among other functionalities, it offers arithmetic operations,
	string representation and instantiation from a string representation.
	"""

	def __init__(self, hours, minutes):
		"""
		The constructor needs the number of hours and the number of minutes
		that make a duration. Give two negative arguments to make a negative
		duration.

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
		elif hours == 0 and minutes == 0:
			self._sign = 0
		else:
			self._sign = 1

		self._hours = abs(hours)
		self._minutes = abs(minutes)
		self._regularize()

	def __abs__(self):
		return HM_Duration(self._hours, self._minutes)

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
		"""
		Determines whether this duration is greater than or equal to another.

		Args:
			other (HM_Duration): another duration

		Returns:
			bool: True if this duration is greater than or equal to the other,
				False otherwise or if other is not an instance of this class
		"""
		if not isinstance(other, self.__class__):
			return False

		return self.to_minutes() == other.to_minutes()

	def __ge__(self, other):
		"""
		Determines whether this duration is greater than or equal to another.

		Args:
			other (HM_Duration): another duration

		Returns:
			bool: True if this duration is greater than or equal to the other,
				False otherwise

		Raises:
			TypeError: if other is not an instance of this class
		"""
		HM_Duration._raise_except_if_wrong_class(other)
		return self.to_minutes() >= other.to_minutes()

	def __gt__(self, other):
		"""
		Determines whether this duration is greater than another.

		Args:
			other (HM_Duration): another duration

		Returns:
			bool: True if this duration is greater than the other,
				False otherwise

		Raises:
			TypeError: if other is not an instance of this class
		"""
		HM_Duration._raise_except_if_wrong_class(other)
		return self.to_minutes() > other.to_minutes()

	def __le__(self, other):
		"""
		Determines whether this duration is lesser than or equal to another.

		Args:
			other (HM_Duration): another duration

		Returns:
			bool: True if this duration is lesser than or equal to the other,
				False otherwise

		Raises:
			TypeError: if other is not an instance of this class
		"""
		HM_Duration._raise_except_if_wrong_class(other)
		return self.to_minutes() <= other.to_minutes()

	def __lt__(self, other):
		"""
		Determines whether this duration is lesser than another.

		Args:
			other (HM_Duration): another duration

		Returns:
			bool: True if this duration is lesser than the other,
				False otherwise

		Raises:
			TypeError: if other is not an instance of this class
		"""
		HM_Duration._raise_except_if_wrong_class(other)
		return self.to_minutes() < other.to_minutes()

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

	def __neg__(self):
		hours = -self.hours
		minutes = -self.minutes
		return HM_Duration(hours, minutes)

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

	@staticmethod
	def from_str(dur_str):
		"""
		Creates an instance from the given duration string representation.

		Args:
			dur_str (str): a string that represents a duration in hours and
				minutes

		Returns:
			HM_Duration: the duration represented by dur_str

		Raises:
			ValueError: if str_repr_duration(dur_str) returns False
		"""
		hours, minutes = duration_from_str(dur_str)
		return HM_Duration(hours, minutes)

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

	@classmethod
	def _raise_except_if_wrong_class(cls, value):
		"""
		Raises a TypeError if the given value is not an instance of this class.

		Args:
			value: any object

		Raises:
			TypeError: if value is not an instance of this class
		"""
		if not isinstance(value, cls):
			raise TypeError("The given object is not of type "
				+ cls.__name__ + ".")

	def _regularize(self):
		"""
		Makes sure that the number of minutes ranges from 0 to 59.
		"""
		self._hours += self._minutes // _MINS_IN_HOUR
		self._minutes = self._minutes % _MINS_IN_HOUR

	@property
	def sign(self):
		"""
		This read-only property returns an integral number that represents the
		sign of this duration: -1 if negative, 0 if null or 1 if positive.
		"""
		return self._sign

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
