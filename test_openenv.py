import openenv.core
with open('c:/Users/seela/Desktop/openenv-project/output.txt', 'w') as f:
    f.write(str(dir(openenv.core)))
try:
    from openenv.core import OpenEnv
    with open('c:/Users/seela/Desktop/openenv-project/output.txt', 'a') as f:
        f.write('\nOpenEnv exists!')
except Exception as e:
    with open('c:/Users/seela/Desktop/openenv-project/output.txt', 'a') as f:
        f.write('\nError: ' + str(e))
