# Thesis
![The project skeleton](./documents/Thesis_Repository.png)
The project is structured in two main folders

 - client side
 - server side
The client_side has the following
 - src
	 - adapters
		 - Holds the gRPC files. 
		 - grpc_client.py is the client interface that gets the data and contacts the server. 
	 - helpers
		 - repository_queues.py
			 - Holds the queues used for the repository. 
		 - data_class.py
			 - Holds the dataclass which formats the data on the client side. 
	 - repository
		 - Holds the same set of codes once run using threads and once using asyncIO. 
		 - asyncIO is the solution most likely to be used afterwards. 
		 - It stores the data in csv files and in an sqlite database. 
		 - The entry point to this folder and its codes is *repository_handler.py 
	 - usecase 
		 - processing.py
			 - Holds the processing where the future pipeline will be implemented. 
		 - run_use_case.py
			 - Holds the whole code base for the usecase. 
			 - It is injected by the grpc_client and by the repository_handler. 
			 - It calls the functions from the client to receive the data, passes it to the repository to store it and then passes it to the processor to process the data. 
			 -  To run the asyncIO repository solution include
				 - from client_side.src.repository.async_repository_handler import Storage
			 - To run the threaded repository solution include
				 - from client_side.src.repository.repository_handler import Storage  
 - main.py
	 - Runs the code for the threaded version.
 - main_async_repo.py
	 - Runs the code for the asyncIO version.
The server_side has the following
 - src
	 - adapters
		 - The gRPC server files and codes.
	 - helpers
		 - The queues used, and the configurations that will be needed.
	 - eeg_api
		 - Will hold the eeg_api codes, but is just a placeholder that generates numpy arrays. 
 - main.py
	 - Runs the server_side codes

