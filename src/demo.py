import numpy as np

from optlib.optimization.optimizationoperator import OperatorDE
from optlib.optimization.optimizer import BasicOptimizer
from optlib.optimization.problem import Sphere
from optlib.optimization.selector import MinSelector
from optlib.optimization.solution import make_objs

# 差分進化を用いてSphere関数問題を最適化するデモを行います。
problem = Sphere(n=100, m=1, d=2, max_fe=10000)
operator = OperatorDE(CR=0.9, F=0.5)
selector = MinSelector()

alg = BasicOptimizer(problem=problem, operator=operator, selector=selector)
alg.run()

print(make_objs(alg.result))
print(np.min(make_objs(alg.result)))
