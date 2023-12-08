import os
import sys
import time

i = 0

def restart():
    import sys
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    import os
    os.execv(sys.executable, ['python'] + sys.argv)

print("Coucou ", i)
i += 1
print("Coucou ", i)
i += 1
print("Coucou ", i)
time.sleep(1)
restart()