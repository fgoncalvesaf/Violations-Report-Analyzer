'''
* Author: Francisco Goncalves de Almeida Filho
* 
* Engenharia de Computacao
* Universidade Federal do Ceara
* TCC - Code Smells
*
* ...
'''
import os
import xml.etree.ElementTree

path = "" #the output path goes here
id_rules = {}
id_severity = {}
for root, dirs, files in os.walk(path):
	for name in files:
		if name.endswith((".xml")):
			violations = xml.etree.ElementTree.parse(root+'/'+name).getroot()
			output_log_path = root+'/'+name+'_log.txt'
			with open(output_log_path, "w") as f:
				f.write("***********************************************************\n")
				f.write('*  '+name+" - ANALYSE\n")
				f.write("***********************************************************\n")
				f.close()
			for file_name in violations.findall('file'):
				with open(output_log_path, "a") as f:
					f.write("\n====\nFile - "+str(file_name.get('name'))+":\n")
					f.close()
				rules_in_file = {}
				for violation in file_name.findall('violation'):
					if str(violation.find('rule').get('id')) not in id_rules:
						id_rules[str(violation.find('rule').get('id'))] = str(violation.find('rule').get('name'))
						id_severity[str(violation.find('rule').get('id'))] = str(violation.find('severity').text)
					if str(violation.find('rule').get('id')) in rules_in_file:
						rules_in_file[str(violation.find('rule').get('id'))] = rules_in_file[str(violation.find('rule').get('id'))] + 1
					else:
						rules_in_file[str(violation.find('rule').get('id'))] = 1
				for key, value in rules_in_file.items():
					with open(output_log_path, "a") as f:
						f.write("\t--\n\tRule "+key+' - '+str(id_rules[key])+": "+str(value)+"\n")
						f.write("\tSeverity: "+str(id_severity[key])+"\n")
						f.close()