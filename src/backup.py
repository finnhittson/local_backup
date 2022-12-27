import os, string
import shutil

available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
path = 'C:/Users/hitts/Desktop/'
items = os.listdir(path)
backup_path = 'D:/'

def check_items(items, path):
	for item in items:
		if os.path.isdir(path + item):
			new_path = path + item
			check_items(os.listdir(new_path), new_path)
		elif os.path.splitext(item)[1] != '.ini':
			new_path = path + item
			check_file(item, new_path)

def check_file(item, path):
	

check_items(items, path)