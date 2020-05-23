from watchdog.events import FileSystemEventHandler
#handler to get names of new files created
#its cleaned each time values are consulted by master
class Handler(FileSystemEventHandler):
	value=[]

	def get_val(self):
		value=self.value
		self.value=[]
		return value
	
	def set_name(self,file):
		self.value.append(file)
    
	def on_created(self, event):
		#print("\narchivo {} creado".format(event.src_path))
		self.set_name(event.src_path)