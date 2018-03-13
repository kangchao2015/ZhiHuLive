import ConfigParser
import sys

reload(sys) 
sys.setdefaultencoding('utf-8')


cf = ConfigParser.ConfigParser();

cf.add_section('a_new_section') 
cf.set('a_new_section',"a","b");
cf.write(open("aa.txt","w"));

cf.read("aa.txt");
sec = cf.sections();				
print cf.options("a_new_section");	
print cf.items("a_new_section");
print cf.get("a_new_section","");