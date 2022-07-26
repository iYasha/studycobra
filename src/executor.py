import builtins
import os
import sys
from io import StringIO
from typing import Optional


class ForbiddenError(ValueError):

	@staticmethod
	def forbidden(cls, *args, **kwargs):
		raise cls('You use forbidden function!')


class StdoutIO:

	def __init__(self, stdout: Optional[StringIO] = None):
		self.stdout = stdout or StringIO()
		self.old_stdout = sys.stdout

	def __enter__(self):
		sys.stdout = self.stdout
		return self.stdout

	def __exit__(self, exc_type, exc_value, traceback):
		sys.stdout = self.old_stdout


class Executor:
	"""
	Simple class for executing python code in a sandbox.
	WARNING: Run only with Docker.
	"""

	forbidden_scope = {"exec": ForbiddenError.forbidden, "eval": ForbiddenError.forbidden}

	def __init__(self, code: str):
		self.code = code
		self.execute_command = exec
		os.system = ForbiddenError.forbidden
		builtins.eval = ForbiddenError.forbidden
		builtins.exec = ForbiddenError.forbidden

	def execute(self):
		with StdoutIO() as out:
			try:
				self.execute_command(self.code, self.forbidden_scope, self.forbidden_scope)
			except ForbiddenError as e:
				print("Something wrong with the code: " + str(e))
		return out.getvalue()


data = Executor(open('main.py').read()).execute().strip()
