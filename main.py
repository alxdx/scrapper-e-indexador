from watcher.Handler import Handler
from watchdog.observers import Observer
from indexer.indexer import Indexer
from watchdog.events import FileSystemEventHandler
import os



if __name__ == '__main__':
	web_dir_observer = Observer()
	event_handler = Handler()
	web_dir_observer.schedule(event_handler, path='docs_web/')
	web_dir_observer.start()
	nombresDocumentos=os.listdir("docs_web/")
	indexer=Indexer(list(map(lambda x : "docs_web/"+x,nombresDocumentos)))

	try:
		while True:	
			word=input("----ingresa termino a buscar: ")
			indexer.searchIndex(word)
			
			is_change=event_handler.get_val() #check if new files were created & get names collected by handler
			if len(is_change) is not 0:
				indexer.update_indexer(is_change)
	except KeyboardInterrupt:
		web_dir_observer.stop()
	# sleep until keyboard interrupt, then stop + rejoin the observer
	web_dir_observer.join()