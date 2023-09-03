import os, string
import shutil
import time
from datetime import datetime
import argparse
import re

# specify defaults by manually changing lists
ignore_dirs = ['github', 'adobe', 'arduino', 'custom office templates', 'for all mankind']
ignore_files = []
target_dirs = ['Documents', 'Desktop']

def check_items(path, top_level):
	items = os.listdir(path)
	update_log = []

	def backup_dir(dir_name, path, update_log):
		if dir_name not in os.listdir(path):
			os.mkdir(os.path.join(path, dir_name))
			update_log.append(f'created dir - {os.path.join(path, dir_name)}')
		return update_log

	def backup_item(item, source, destination, m_time, update_log):
		if item not in os.listdir(destination) or m_time > last_upt:
			shutil.copy(source, destination)
			update_log.append(f'copied file - {os.path.join(source)}')
		return update_log

	for item in items:
		item_path = os.path.join(path, item)
		if os.path.isdir(item_path) and item.lower() not in ignore_dirs:
			update_log = backup_dir(item, top_level, os.path.getmtime(item_path), update_log)
			update_log += check_items(item_path, os.path.join(top_level, item))
		elif not os.path.isdir(item_path) and os.path.splitext(item)[1] != '.ini' and item.lower() not in ignore_files:
			update_log = backup_item(item, item_path, top_level, os.path.getmtime(item_path), update_log)
	
	return update_log

def remove_items(path, backup_path):
	items = os.listdir(backup_path)
	remove_log = []
	for item in items:
		local_items = os.listdir(path)
		backup_item_path = os.path.join(backup_path, item)
		if os.path.isdir(backup_item_path):
			if item not in local_items or item.lower() in ignore_dirs:
				try:
					shutil.rmtree(backup_item_path)
					remove_log.append(f'removed dir - {backup_item_path}')
				except:
					pass
			else:
				remove_items(os.path.join(path, item), backup_item_path)
		elif item not in local_items or item.lower() in ignore_files:
			try:
				os.remove(backup_item_path)
				remove_log.append(f'removed file - {backup_item_path}')
			except:
				pass
	return remove_log

def write_to_log(backup_drive, update_log, remove_log):
	with open(os.path.join(backup_drive, "log.txt"), "w") as f:
		update_time = time.time()
		f.write(f"Last update time: {update_time}\n")
		timestamp = datetime.fromtimestamp(update_time)
		f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
		if len(update_log) == 0 and len(remove_log) == 0:
			f.write("\nAll files up to date.\n")
		else:
			if len(update_log) != 0:
				f.write("\nUpdates:\n")
				for update in update_log:
					f.write(f"{update}\n")

			if len(remove_log) != 0:
				f.write("\nRemoved:\n")
				for remove in remove_log:
					f.write(f"{remove}\n")

if __name__ == '__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument(
		"--backup-loc",
		default="E",
		type=str)
	argparser.add_argument(
		"-v", 
		"--verbose",
		action="store_true")
	args = argparser.parse_args()

	backup_drive = args.backup_loc + ":\\"

	if args.verbose:
		print(f"Backup drive: \"{backup_drive}\"")
		if target_dirs:
			print("Default target directories: ", "\\, ".join(target_dirs) + "\\")
		if ignore_files:
			print("Ignoring files: ", ", ".join(ignore_files))
		if ignore_dirs:
			print("Ignoring directories: ", "\\, ".join(ignore_dirs) + "\\")

	last_upt = 0
	log_file = os.path.join(backup_drive, "log.txt")
	if os.path.exists(log_file):
		f = open(log_file, 'r')
		last_upt = float(re.search("[0-9]*\\.[0-9]*$", f.readline()).group(0))
		f.close()
		os.remove(log_file)

	path = 'C:\\Users\\hitts\\'
	update_log = []
	remove_log = []
	if True:
		available_drives = ["%s:\\" % d for d in string.ascii_uppercase if os.path.exists("%s:" % d)]
		if backup_drive in available_drives:
			for target_dir in target_dirs:
				backup_target_dir = os.path.join(backup_drive, target_dir)
				local_target_dir = os.path.join(path, target_dir)
				if not os.path.isdir(backup_target_dir):
					os.makedirs(os.path.join(backup_drive, target_dir))
				update_log += check_items(local_target_dir, backup_target_dir)
				remove_log += remove_items(local_target_dir, backup_target_dir)
	write_to_log(backup_drive, update_log, remove_log)
