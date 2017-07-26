import os
import shutil

src = r'C:\Users\Mostapha\Documents\code\ladybug-tools\honeybee-dynamo'
dst = r'C:\Users\Mostapha\AppData\Roaming\Dynamo\Dynamo Revit\1.3\packages\Honeybee'

os.chdir(src)

# copy definitions
dyfs = (f for f in os.listdir('plugin\\dyf') if f.endswith('.dyf'))
for f in dyfs:
    shutil.copy(os.path.join(src, 'plugin\\dyf\\%s' % f), dst + '\\dyf')

# copy source files
srcs = (f for f in os.listdir('plugin\\src') if f.endswith('.py'))

for s in srcs:
    shutil.copy(os.path.join(src, 'plugin\\src\\%s' % s), dst + '\\extra\\nodesrc')

# # honeybee source code
# files = (f for f in os.listdir('honeybee') if f.endswith('.py'))
#
# for f in files:
#     shutil.copy(os.path.join(src, 'honeybee\\%s' % f), dst + '\\extra\\honeybee')
