# coding=utf-8
import sys
from glob import glob
from pydub import AudioSegment
reload(sys) 
sys.setdefaultencoding('utf-8')



a = [AudioSegment.from_file(name)for name in glob("./m4a/*.m4a") ];
count = 0;
for z in a:
	if count == 0:
		s = z;
	else:
		s = s.append(z);
	count += 1;

file_handle = s.export("./aa.wav", format="wav")