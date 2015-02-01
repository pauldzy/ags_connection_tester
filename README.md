arcgis_server_connection_tester.py

Arcpy script which seeks to validate connections both in your ArcCatalog desktop and on your AGS server(s).

NOTE: in this and all my scripts, all security is wrapped up within your existing ArcCatalog connections.  The script knows nothing about your passwords or servers and only takes as input the names of the connections as you have them so titled in ArcCatalog.  

Provide the script a list of your ArcGIS Server admin connections and list of SDE database connections and test that all connections are valid for your desktop and test that all SDE database connections are valid on all ArcGIS Servers.

The script is meant to troubleshoot situations where deployments fail and it not immediately clear where the problem lies.  For geoprocessing deployments in particular there are many points of failure both local to the deployer and remote at the ArcGIS Server.  All portions of a geoprocessing service must be executed on the local desktop before being pushed to the service.  For AGS 10.2.2 it is unfortunately quite easy to deploy a geoprocessing service that runs fine locally but with dead database connections at the server.  Your first notification of this condition will occur only after calling the service fails.

Initial Steps:

   1) The script first checks that the list of ArcGIS Server admin connections all exist (the .ags files themselves).
   
   2) A ListDataStoreItems command is run against each connection to verify that it functions.  We assume you have at least one folder datastore.  Perhaps there is a better test but the interface is rather sparse.
   
   3) Then the list of SDE database connections are checked if they exist (the .sde files themselves).
   
   4) A ListFeatureClasses command is run against each connection to verify that it functions.  We assume you have at least one feature class visible.  
   
So with this stage complete we can say that the universe of connections exists and whether they are valid.  If all items succeed then its a good bet the geoprocessing service execution will succeed locally (or rather any problems are not with the connections).  Unfortuneately this is no guarantee that the ArcGIS Server will also be able to utilize the same set of SDE connections.
   
AGS database checks:

   1) For connections that survive the initial steps, we harvest the username and instance string from the SDE connections and compare them to the usernames and instance strings of existing data stores on the AGS server.  If they match, then we execute ValidateDataStoreItem against the data store and report the results.
   
   2) If there is no match found, then we create a temporary data store on the server whose name is configurable from the variable at the top of the script.  The creation of the new data store item validates the connection.  Note the current error exception handling is quite poor (10.2.2) as creating the data store does not report back anything, good or bad.  So we have to then check if the data store exists afterwards as confirmation of the validity.  
   
   3) Note that the arcpy data store creation step itself is rather buggy.  You cannot import via arcpy the same .sde connection file name twice.  One approach we had been using was to rename the .sde connection as needed depending on the server deployment.  This fails as if you load X.sde with data store name FOO having parameters A and then try to load X.sde withe data store name YADA and parameters B, the import will fail as apparently either the server or the desktop stashes these .sde files somewhere and is not intellegent enough to rename them if that file name already exists.  This is a long-winded explanation for why the script copies the .sde connection file and makes a temporary copy of the .sde file with a unique guuid filename.    

If all steps are successfull then you can be somewhat assured that the environment on the deployer's desktop and ArcGIS Server is correct for your service.  This should allow you to target your further troubleshooting.

Feedback is always welcome.


