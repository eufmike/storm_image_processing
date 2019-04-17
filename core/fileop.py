import os, sys, re

def DirCheck(targetpaths):
	"""
	dircheck checks the target folder and create the folder if it does not exist.
	targetdirlist: list of folderpath
	"""
	# print(type(targetpaths))
	if isinstance(targetpaths, str): 
		print(os.path.exists(targetpaths))
		if not os.path.exists(targetpaths):
			os.makedirs(targetpaths)
	elif isinstance(targetpaths, list): 
		for path in targetpaths:
			if not os.path.exists(path):
				os.makedirs(path)

def ListFiles(path, extension = None):
	filelist = []
	fileabslist = []
	for directory, dir_names, file_names in os.walk(path):
		# print(file_names)
		
		for file_name in file_names:
			if (not file_name.startswith('.')) & (file_name.endswith(extension)):
				file_name_base = file_name.replace(extension, '')
				filepath_tmp =  os.path.join(directory, file_name)
				filelist.append(file_name_base)
				fileabslist.append(filepath_tmp)
	
	return {'filelist': filelist,
			'fileabslist': fileabslist}

def GetPendingList(src_dir, op_dir, src_ext = '.nd2', op_ext = '.csv'):
	"""
	getpendinglist compares the files from src_dir and the accomplisjed file in op_dir, 
	then creates a pending list of unprocessed image. 
	"""
	
	srclist = ListFiles(src_dir, src_ext)
	srclist = srclist['fileabslist']
	oplist = ListFiles(op_dir, op_ext)
	oplist = oplist['fileabslist']

	oplist_basename = []
	for i in oplist:
		name = os.path.basename(i)
		# print('name: {}'.format(name))
		basename = os.path.splitext(name)[0]
		# print('basename: {}'.format(basename))
		oplist_basename.append(basename)
	
	pendingfllist = []
	pendingpathlist_input = []
	pendingpathlist_output = []
	
	for i in range(len(srclist)):
		srcflname = os.path.basename(srclist[i])
		srcflbasename = os.path.splitext(srcflname)[0]
		
		if not srcflbasename in oplist_basename:
			pendingfllist.append(srcflbasename)
			pendingpathlist_input.append(srclist[i])			
			pendingpathlist_output.append(os.path.join(op_dir, srcflbasename + op_ext))
			
	return (pendingfllist, pendingpathlist_input, pendingpathlist_output)


def GetGrpFLs(filenamelist, nchannels, group: dict, ippath: dict, oppath: dict):
	mainflls = {}
	
	for c in range(nchannels):
		mainflls[str(c+1)] = {}
		for g in group.keys():
			mainflls[str(c+1)][g] = {}    
			
			# create list
			filename_tmp = []
			
			for l in filenamelist: 
				grp_code = group[g]
				x = re.search('(.*)_'+ grp_code + '{1}[0-9]{1}_(.*)', l)
				try: 
					found = x.group(0)
					filename_tmp.append(found)
				except AttributeError:
					found = ''

			# create input filelist and input path
			filepath_ip = []
			for f in filename_tmp: 
				filepath_ip_tmp =  os.path.join(ippath['dir'], str(c+1), f + ippath['ext'])
				filepath_ip.append(filepath_ip_tmp)
			
			mainflls[str(c+1)][g]['filename_ip'] = filename_tmp
			mainflls[str(c+1)][g]['filepath_ip'] = filepath_ip

			filepath_op = {}

			# create output path
			for key in oppath.keys():
				filepath_op = []
				for f in filename_tmp:	
					filename_op_tmp = f.replace(ippath['ext'], oppath[key]['ext'])
					path_op_tmp = os.path.join(oppath[key]['dir'], str(c+1), filename_op_tmp)
					filepath_op.append(path_op_tmp)

				mainflls[str(c+1)][g][key] = filepath_op	

	return(mainflls)
	