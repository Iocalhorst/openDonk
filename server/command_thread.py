from threading import Thread,Event
import time

"""
	cli prompt utility class, nonblocking input parsing and some basic handing.
																						 """

class CommandThread(Thread):
	def __init__(self, args=None, kwargs=None):
		Thread.__init__(self,group=None,daemon=True)
		self.daemon=True
		self.finished=Event()
		self.list_commands=[]
		self.available_commands=["start", "create table", "stop", "exit", "info", "help"]
		self.hint="available commands   :  start, stop, create table, exit, info ,help"
	def cancel(self):
		self.finished.set()
	def run(self):
		print(self.hint)
		while not self.finished.is_set() :
			while self.has_command():
				time.sleep(0.5)
			cmd=input(">")
			if cmd not in self.available_commands :
				print(self.hint)
			else :
				if cmd=="help":
					self.print_help()
				else :
					self.list_commands.append(cmd)
		time.sleep(0.5)
	def has_command(self):
		if len(self.list_commands) > 0 :
			return True
		return False
	def get_command(self):
		assert len(self.list_commands)>0,"Error [CommandThread] get_command on empty list - use .has_command() beforehand"
		cmd=self.list_commands.pop(0)
		return cmd

	def print_help(self):
		print(self.hint)
		#new_help  =" new   :  create a new server_thread instance"
		start_help="start  :  quick seat players - for testing client view update. subsciption seems to be ok"
		create_table_help="create table :  create a table instance"
		stop_help =" stop  :  tell the server_thread to stop the listener, then it kills the thread"
		exit_help =" exit  :  exit this program, TODO : cleanup"
		info_help =" info  :  TODO!"
		help_help =" help  :  display this screen"
		pad="             "
		#print(self.hint)
		#print(pad,new_help)
		print(pad,start_help)
		print(pad,create_table_help)
		print(pad,stop_help)
		print(pad,info_help)
		print(pad,exit_help)
		print(pad,help_help)
