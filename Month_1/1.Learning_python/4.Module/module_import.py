
print("read for all possible ways to import files and methods and their best practices")
import module_export
module_export.fib(10)
from module_export import fib
fib(10)
from module_export import *   # discouraged (pollutes namespace)
import module_export as fb    # alias
from module_export import fib as module_export #fibonacci number 

import sys
sys.path.append("./extras")
# from extras import other_path_func
# from extras import other_path_func


other_path_func()
