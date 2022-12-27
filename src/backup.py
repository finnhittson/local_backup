import os, string
import shutil
import time

def check_items(path, toplevel, lu_time, ignore_files, ignore_dirs):
	items = os.listdir(path)

	def backup_dir(dir_name, path, mtime):
		if dir_name not in os.listdir(path) or mtime > lu_time:
			os.mkdir(path + dir_name)
			print('copied dir')

	def backup_item(item, source, destination, mtime):
		if item not in os.listdir(destination) or mtime > lu_time:
			shutil.copy(source, destination)
			print('copied file')

	for item in items:
		if os.path.isdir(path + item) and item not in ignore_dirs:
			backup_dir(item, toplevel, os.path.getmtime(path + item))
			new_path = path + item + "/"
			check_items(new_path, toplevel + item + "/", lu_time, ignore_files, ignore_dirs)
		elif os.path.splitext(item)[1] != '.ini' and item not in ignore_files:
			backup_item(item, path + item, toplevel, os.path.getmtime(path + item))

def remove_items(path, backup_path):
	items = os.listdir(backup_path)
	for item in items:
		local_items = os.listdir(path)
		if os.path.isdir(backup_path + item):
			if item not in local_items:
				shutil.rmtree(backup_path + item)
				print('removed dir')
			else:
				remove_items(path + item + '/', backup_path + item + '/')
		elif item not in local_items:
			os.remove(backup_path + item)
			print('removed file')


if __name__ == '__main__':
	run = 1
	ignore_files = []
	ignore_dirs = ['github']
	backup_dirs = ['Desktop/']
	path = 'C:/Users/hitts/'
	backup_path = 'D:/'
	while run:
		lu_time = time.time()
		available_drives = ['%s:/' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
		if backup_path in available_drives:
			print('available for backup')
			for backup_dir in backup_dirs:
				check_items(path + backup_dir, backup_path, lu_time, ignore_files, ignore_dirs)
				remove_items(path + backup_dir, backup_path)
		#time.sleep(3600)
		run = 0