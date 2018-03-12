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

id_rules = {}
id_severity = {}
for root, dirs, files in os.walk("./"):
	for name in files:
		if name.endswith((".xml")):
			violations = xml.etree.ElementTree.parse(root+'/'+name).getroot()
			output_log_path = root+'/'+name+'_log.txt'
			with open(output_log_path, "w") as f:
				f.write("***********************************************************\n")
				f.write('*  '+name+" - ANALYSIS\n")
				f.write("***********************************************************\n")
				f.close()
			project_rules_id_quantity = {}
			files_analized = 0
			total_violations = 0
			print('Analyzing report '+name)
			for file_name in violations.findall('file'):     #iter files
				with open(output_log_path, "a") as f:
					f.write("\n====\nFile - "+str(file_name.get('name'))+":\n")
					f.close()
				rules_in_file = {}
				files_analized = files_analized + 1
				for violation in file_name.findall('violation'): #iter violations in a file
					if str(violation.find('rule').get('id')) not in id_rules:
						id_rules[str(violation.find('rule').get('id'))] = str(violation.find('rule').get('name'))
						id_severity[str(violation.find('rule').get('id'))] = str(violation.find('severity').text)
					if str(violation.find('rule').get('id')) in project_rules_id_quantity:
						project_rules_id_quantity[str(violation.find('rule').get('id'))] = project_rules_id_quantity[str(violation.find('rule').get('id'))] + 1
						total_violations = total_violations + 1
					else:
						project_rules_id_quantity[str(violation.find('rule').get('id'))] = 1
						total_violations = total_violations + 1	
					if str(violation.find('rule').get('id')) in rules_in_file:
						rules_in_file[str(violation.find('rule').get('id'))] = rules_in_file[str(violation.find('rule').get('id'))] + 1
					else:
						rules_in_file[str(violation.find('rule').get('id'))] = 1	
				for key, value in rules_in_file.items():
					with open(output_log_path, "a") as f:
						f.write("\t--\n\tRule "+key+' - '+str(id_rules[key])+": "+str(value)+"\n")
						f.write("\tSeverity: "+str(id_severity[key])+"\n")
						f.close()
			with open(output_log_path, "a") as f:
					f.write("\n***********Project Overview***********")
					f.write("\nNumber of files with violations: "+str(files_analized))
					f.write("\nNumber of violations found: "+str(total_violations))
					f.close()
			for key, value in project_rules_id_quantity.items():
				with open(output_log_path, "a") as f:
					if len(key) < 2:
						f.write("\nRule: 0"+key+"\t-\t"+str(value)+"\t|\tSeverity:"+id_severity[key]+"\t"+id_rules[key])
					else:
						f.write("\nRule: "+key+"\t-\t"+str(value)+"\t|\tSeverity:"+id_severity[key]+"\t"+id_rules[key])
					f.close()
print('Done!')