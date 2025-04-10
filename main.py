from bugly import var_ins, func_ins, live_trace
import time

x = 0
var_ins("x")

@func_ins
def greet(name):
    return f"Hello, {name}"

for i in range(3):
    x = i
    msg = greet(f"User{i}")
    print(msg)
    time.sleep(1)

live_trace()
