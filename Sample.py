from start_compiler import import_start

import_start.LONG_NAMES = False

attrlist = dir(import_start)
for attr in attrlist:
	if attr[:2] != '__':
		globals()[attr] = getattr(import_start, attr)


class coordinate(Start):
	type = {'x': 'number', 'y': 'number'}
	def __init__(self, args0=None, args1=None):
		super().__init__()
		self.x = number()
		self.x = self.x if args0 is None else args0
		self.y = number()
		self.y = self.y if args1 is None else args1
local_vars['point_a'] = coordinate()
local_vars['point_b'] = coordinate()
local_vars['point_a'] = coordinate(number(1), number(1))
setattr(local_vars['point_b'], 'x', number(2))
setattr(local_vars['point_b'], 'y', number(2))

if _lt(getattr(local_vars['point_a'], 'x'), number(5)):
	setattr(local_vars['point_a'], 'y', number(10).clone())

_print(local_vars['point_a'], local_vars['point_b'])
