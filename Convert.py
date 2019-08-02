#!/usr/bin/python
#	 pip install requests
import requests
import sys
import os

input_dir = "HTML"              # Sub folder of webfiles
output_dir = "HTML_minified"

try:
	sys.argv[1]
except NameError:
	f_output = 'output_dir'
else:
	f_output = sys.argv[1]
print("Using outputfile: " + f_output)

f_output = open(f_output, "w")
# f_output = open("output_dir", "w")
URL_minify_js   = 'https://javascript-minifier.com/raw' # Website to minify javascript
URL_minify_html = 'https://html-minifier.com/raw'        # Website to minify html
URL_minify_css  = 'https://cssminifier.com/raw'         # Website to minify css

def write_to_file(file, data, dir=""):
    filename, file_extension = os.path.splitext(file)       # Split filename and file extension
    file_extension = file_extension.replace(".","")         # Remove puncuation in file extension

    dir = dir.replace(input_dir,"")                         # Remove the first directory(input_dir)
    dir = dir.replace("\\","/")                             # Chang to /
    f_output.write("// " + dir + "\n")                      # Print comment
    f_output.write("const char* data_" + filename + "_" + file_extension + "_path PROGMEM = \""+str(dir)+"\";\n")	# print path
    f_output.write("const char data_"+filename+"_"+file_extension+"[] PROGMEM = {"+data.upper()+"};\n")			# print binary data
    f_output.write("#define " + ("data_" + filename + "_len " + str(data.count('0x'))).upper() + "\n\n")

def file2Hex(filename):
    output_str = ""
    x = 1
    myfile = open(filename, "rb")
    try:
	binLen = os.path.getsize(filename)
	byte = myfile.read(1)

	while byte != "":
            output_str += hex(ord(byte))
            if (x != binLen):
		output_str += ","
            x += 1
	    # Next Byte 
	    byte = myfile.read(1)
    finally:
	myfile.close()
    return output_str

def aschii2Hex(text):
    output_str = ""
    x = 1
    strLen = len(text)
    for character in text:
        output_str += hex(ord(character))

        if (x != strLen):
            output_str += ","
        x += 1
    return output_str

def minify_js(input_file):
    url = URL_minify_js
    data = {'input': open(input_file, 'rb').read()}
    response = requests.post(url, data=data)
    return response.text

def minify_html(input_file):
    url = URL_minify_html
    data = {'input': open(input_file, 'rb').read()}
    response = requests.post(url, data=data)
    return response.text

def minify_css(input_file):
    url = URL_minify_css
    data = {'input': open(input_file, 'rb').read()}
    response = requests.post(url, data=data)
    return response.text

def process_file(dirname, filename, fullfilename):
    if filename.endswith(".js"):
	print("Output JAVASRIPT: " + fullfilename)
	minified = minify_js(fullfilename)          # minify javascript
	hexified = aschii2Hex(minified)                         # convert to hex
    elif filename.endswith(".html"):
	print("Output HTML: " + fullfilename)
	minified = minify_html(fullfilename)        # minify html
	hexified = aschii2Hex(minified)                         # convert to hex
    elif filename.endswith(".css"):
	print("Output CSS: " + fullfilename)
	minified = minify_css(fullfilename)         # minify css
	hexified = aschii2Hex(minified)                         # convet to hex
    elif filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".gif"):
	print("Output IMAGE: " + fullfilename)
	hexified = file2Hex(fullfilename) # convert file to hex
    else: 
	# ignore other files
	print("Ignore File: " + fullfilename)
	return

    # Output to file
    if len(dirname) > 0: 
	write_to_file( dirname + "_" + filename , hexified, fullfilename) # write to file
    else :
	write_to_file( filename , hexified, fullfilename) # write to file


for root, dirs, files in os.walk(input_dir, topdown=False):
    #Process Files
    for filename in files:   # for files
	fullfilename = os.path.join(root, filename)
	dirname = fullfilename.rsplit('/', 1)[0].strip(input_dir + "/") #Get Dirname
	process_file(dirname, filename, fullfilename)
 
f_output.close()