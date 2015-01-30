arcgis_server_connection_tester.py

Arcpy script which seeks to validate connections both in your ArcCatalog desktop and on your AGS server(s).

Provide the script a list of your ArcGIS Server admin connections and list of SDE database connections and test that all connections are valid for your desktop and test that all SDE database connections are valid on all ArcGIS Servers.

The script is meant to troubleshoot situations where deployments fail and it not immediately clear where the problem lies.  For geoprocessing deployments in particular there are many points of failure both local to the deployer and remote at the ArcGIS Server.  For AGS 10.2.2 it is unfortunately quite easy to deploy a geoprocessing server with dead database connections.

Initial Steps:

   1) The script first checks that the list of ArcGIS Server admin connections all exist.
   
   2) A ListDataStoreItems command is run against each connection to verify that it functions.  We assume you have at least one folder datastore.  
   
   3) Then the list of SDE database connections are checked if they exist.
   
   4) A ListFeatureClasses command is run against each connection to verify that it functions.  We assume you have at least one feature class visible.
   
AGS database checks:

   1) For connections that survive the initial steps 


