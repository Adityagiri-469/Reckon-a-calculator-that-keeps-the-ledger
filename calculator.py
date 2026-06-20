import ast
import math
import operator as op
import sys
import pathlib


# Safe evaluator supporting math functions, variables, and assignments
class SafeEval(ast.NodeVisitor):
	def __init__(self, variables=None):
		self.vars = {} if variables is None else variables

	def visit(self, node):
		method = 'visit_' + node.__class__.__name__
		return getattr(self, method, self.generic_visit)(node)

	def visit_Module(self, node):
		if len(node.body) != 1:
			raise ValueError('Only single expressions or assignments are allowed')
		return self.visit(node.body[0])

	def visit_Expr(self, node):
		return self.visit(node.value)

	def visit_Assign(self, node):
		if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
			raise ValueError('Only simple assignments to variables are allowed')
		name = node.targets[0].id
		value = self.visit(node.value)
		self.vars[name] = value
		return value

	def visit_BinOp(self, node):
		left = self.visit(node.left)
		right = self.visit(node.right)
		return _BINOPS[type(node.op)](left, right)

	def visit_UnaryOp(self, node):
		operand = self.visit(node.operand)
		return _UNARYOPS[type(node.op)](operand)

	def visit_Call(self, node):
		if not isinstance(node.func, ast.Name):
			raise ValueError('Only direct function calls allowed')
		func_name = node.func.id
		if func_name not in _MATH_FUNCS:
			raise NameError(f"Unknown function: {func_name}")
		args = [self.visit(a) for a in node.args]
		return _MATH_FUNCS[func_name](*args)

	def visit_Name(self, node):
		if node.id in self.vars:
			return self.vars[node.id]
		if node.id in _MATH_FUNCS:
			return _MATH_FUNCS[node.id]
		raise NameError(f"Unknown variable or function: {node.id}")

	def visit_Constant(self, node):
		return node.value

	def visit_Num(self, node):
		return node.n

	def generic_visit(self, node):
		raise ValueError(f'Unsupported expression: {node!r}')


# Supported operations
_BINOPS = {
	ast.Add: op.add,
	ast.Sub: op.sub,
	ast.Mult: op.mul,
	ast.Div: op.truediv,
	ast.FloorDiv: op.floordiv,
	ast.Mod: op.mod,
	ast.Pow: op.pow,
}

_UNARYOPS = {ast.UAdd: op.pos, ast.USub: op.neg}

# Expose safe math functions
_MATH_FUNCS = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}
_MATH_FUNCS.update({'abs': abs, 'round': round})


def evaluate(expr: str, variables: dict):
	tree = ast.parse(expr, mode='exec')
	evaluator = SafeEval(variables)
	return evaluator.visit(tree)


def repl():
	vars_store = {}
	history = []
	hist_file = pathlib.Path.home() / '.calculator_history'

	# load history if present
	try:
		if hist_file.exists():
			with hist_file.open('r', encoding='utf-8') as f:
				history.extend([l.rstrip('\n') for l in f.readlines() if l.strip()])
	except Exception:
		pass

	print('Simple Calculator REPL — type `help` for commands')
	while True:
		try:
			text = input('calc> ').strip()
		except (EOFError, KeyboardInterrupt):
			print('\nExiting')
			break
		if not text:
			continue
		if text.lower() in ('exit', 'quit'):
			break
		if text.lower() == 'help':
			print('Commands: help, exit, history, vars, clear')
			print('You can assign: x = 2+3 and call functions: sin(1.0)')
			continue
		if text.lower() == 'history':
			for i, h in enumerate(history[-50:], start=1):
				print(f'{i}: {h}')
			continue
		if text.lower() == 'vars':
			for k, v in vars_store.items():
				print(f'{k} = {v}')
			continue
		if text.lower() == 'clear':
			vars_store.clear()
			print('Variables cleared')
			continue

		try:
			result = evaluate(text, vars_store)
			history.append(text)
			if result is not None:
				print(result)
		except Exception as e:
			print('Error:', e)

	# persist history
	try:
		with hist_file.open('a', encoding='utf-8') as f:
			for h in history[-100:]:
				f.write(h + '\n')
	except Exception:
		pass


def main():
	if len(sys.argv) > 1:
		expr = ' '.join(sys.argv[1:])
		try:
			out = evaluate(expr, {})
			if out is not None:
				print(out)
		except Exception as e:
			print('Error:', e)
		return
	repl()


if __name__ == '__main__':
	main()

