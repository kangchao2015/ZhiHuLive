import ConfigParser
import sys
import urllib

def download(url,dir,name=None):

    if name == None:
        defaultName = datetime.datetime.now().strftime('%H:%M:%S');
    else:
        defaultName = name;

	try:
	    if os.path.exists(dir):
	        pass;
	    else:
	        os.mkdirs(dir);

	   	path = os.path.join(dir, defaultName); 
		urllib.urlretrieve(url, path);
		return True;
    except Exception as e:
    	print "error ";
    	return False;


download("https://live-audio.vzuu.com/8587ac14bfacc6060835f5f1d84960f8", "./a.m4a")
# reload(sys) 
# sys.setdefaultencoding('utf-8')


# cf = ConfigParser.ConfigParser();

# cf.add_section('a_new_section') 
# cf.set('a_new_section',"a","b");
# cf.write(open("aa.txt","w"));

# cf.read("aa.txt");
# sec = cf.sections();				
# print cf.options("a_new_section");	
# print cf.items("a_new_section");
# print cf.get("a_new_section","");