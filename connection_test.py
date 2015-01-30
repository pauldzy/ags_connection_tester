import arcpy
import sys,os
import uuid

#------------------------------------------------------------------------------
#
# Connection Test Script
# Version 1.0
#
#------------------------------------------------------------------------------

# Alter these names to fit what you have in your ArcCatalog Connections
arcgis_server_connections = [
    'cat_admin'
   ,'watersgeo_admin'
];

arcsde_database_connections = [
    'rad_ags-owstg'
   ,'rad_ags-owpub'
   ,'rad_ags-waters10'
];

# Temporary Data Store name, change to whatever you like
tmp_data_store = "TMPDZ";

#------------------------------------------------------------------------------
# Step 10
# Initialize the tests
#------------------------------------------------------------------------------
arcpy.AddMessage("Validating ArcCatalog Connections.");
arcpy.AddMessage(" ");
arcpy.AddMessage(
    "Checking " + str(len(arcgis_server_connections)) + " AGS connections and " 
    + str(len(arcsde_database_connections)) + " SDE connections."
);
int_bad = 0;

#------------------------------------------------------------------------------
# Step 20
# Test the ArcGIS Server Connections
#------------------------------------------------------------------------------
ags_good_conn = [];
for agsconn in arcgis_server_connections:
   arcpy.AddMessage(" ");
   arcpy.AddMessage("Testing " + agsconn + ":");
   
   arcpy.AddMessage("   Searching for connection file...");
   boo_good = True;
   
   ags_con = "GIS Servers\\" + agsconn + ".ags";
   if arcpy.Exists(ags_con):
      arcpy.AddMessage("      SUCCESS: " + ags_con);
      
   else:
      ags_con2 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.3\\ArcCatalog\\" + agsconn+ ".ags"
   
      if arcpy.Exists(ags_con2):
         ags_con = ags_con2;
         arcpy.AddMessage("      SUCCESS: " + ags_con);
      
      else:
         ags_con3 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\" + agsconn + ".ags"
         
         if arcpy.Exists(ags_con3):
            ags_con = ags_con3;
            arcpy.AddMessage("      SUCCESS: " + ags_con);
         
         else:  
            ags_con4 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.1\\ArcCatalog\\" + agsconn + ".ags"
         
            if arcpy.Exists(ags_con4):
               ags_con = ags_con4;
               arcpy.AddMessage("      SUCCESS: " + ags_con);
               
            else:
               arcpy.AddMessage("      ERROR: " + agsconn + " not found on this system.");
               boo_good = False;
               int_bad += 1;
   
   if boo_good:
      arcpy.AddMessage("   Counting folder data stores...");
      
      try:
         stores = arcpy.ListDataStoreItems(ags_con,"FOLDER");
      except arcpy.ExecuteError:
         print(arcpy.GetMessages(2));
      
      arcpy.AddMessage("      SUCCESS: Found " + str(len(stores)) + " data stores.");
      ags_good_conn.append(ags_con);
      
#------------------------------------------------------------------------------
# Step 30
# Test the ArcSDE Database Connections
#------------------------------------------------------------------------------
sde_good_conn = [];
for sdeconn in arcsde_database_connections:
   arcpy.AddMessage(" ");
   arcpy.AddMessage("Testing " + sdeconn + ":");
   
   arcpy.AddMessage("   Searching for connection file...");
   boo_good = True;
   
   sde_con = "Database Connections\\" + sdeconn + ".sde";
   if arcpy.Exists(sde_con):
      arcpy.AddMessage("      SUCCESS: " + sde_con);
      
   else:
      sde_con2 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.3\\ArcCatalog\\" + sdeconn + ".sde"
      
      if arcpy.Exists(sde_con2):
         sde_con = sde_con2;
         arcpy.AddMessage("      SUCCESS: " + sde_con);
         
      else:
         sde_con3 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\" + sdeconn + ".sde"
         
         if arcpy.Exists(sde_con3):
            sde_con = sde_con3;
            arcpy.AddMessage("      SUCCESS: " + sde_con);
         
         else:  
            sde_con4 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.1\\ArcCatalog\\" + sdeconn + ".sde"
         
            if arcpy.Exists(sde_con4):
               sde_con = sde_con4;
               arcpy.AddMessage("      SUCCESS: " + sde_con);
            
            else:  
               arcpy.AddMessage("      ERROR: " + sdeconn + " not found on this system.");
               boo_good = False;
               int_bad += 1;

   if boo_good:
      arcpy.AddMessage("   Checking database details...");
      
      try:
         arcpy.env.workspace = sde_con;
      except arcpy.ExecuteError:
         print(arcpy.GetMessages(2));
      
      try:
         desc = arcpy.Describe(sde_con);
         cp = desc.connectionProperties;
      except arcpy.ExecuteError:
         print(arcpy.GetMessages(2));
       
      arcpy.AddMessage("      User    : " + cp.user);
      arcpy.AddMessage("      Instance: " + cp.instance);

      arcpy.AddMessage("   Counting feature classes in database...");
      try:
         fdlist = arcpy.ListFeatureClasses("*");
      except arcpy.ExecuteError:
         print(arcpy.GetMessages(2));    

      if len(fdlist) == 0:
         arcpy.AddMessage("      ERROR: unable to query a list of feature classes.");
         int_bad += 1;
      else:
         arcpy.AddMessage("      SUCCESS: Found " + str(len(fdlist)) + " feature classes.");
         sde_good_conn.append(sdeconn);     

#------------------------------------------------------------------------------
# Step 40
# Test if the AGS Servers can see the SDE connections
#------------------------------------------------------------------------------
arcpy.AddMessage(" ");
if len(ags_good_conn) == 0:
   arcpy.AddMessage("No valid ArcGIS Servers to test connections upon.");
   
elif len(sde_good_conn) == 0:
   arcpy.AddMessage("No valid SDE connections to test on AGS servers.");
   
else:
   arcpy.AddMessage(
      "Validating " + str(len(sde_good_conn)) 
      + " SDE connections on " + str(len(ags_good_conn)) 
      + " AGS servers..."
   );
   
for ags in ags_good_conn:
   arcpy.AddMessage("   Tapping into " + ags);
   
   lst_ds = arcpy.ListDataStoreItems(ags,"DATABASE");
   for ds in lst_ds:
      ds_name = ds[0];
      if ds_name == tmp_data_store:
         arcpy.RemoveDataStoreItem(
             ags
            ,"DATABASE"
            ,tmp_data_store
         );
         
   for sde in sde_good_conn:
      arcpy.AddMessage("      Checking " + sde);
      
      sde_file = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.3\\ArcCatalog\\" + sde + ".sde"
      if not arcpy.Exists(sde_file):
         sde_file = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\" + sde + ".sde"
 
         if not arcpy.Exists(sde_file):
            sde_file = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.1\\ArcCatalog\\" + sde + ".sde"
         
            if not arcpy.Exists(sde_file):
               arcpy.AddMessage("      ERROR: cannot find the " + sde + ".sde file on this system.");
      
      desc = arcpy.Describe(sde_file);
      cp = desc.connectionProperties;
      username = cp.user;
      instance = cp.instance;
      
      ds_match = None;
      lst_ds = arcpy.ListDataStoreItems(ags,"DATABASE");
      for ds in lst_ds:
         ds_name = ds[0];
         ds_details = ds[1].split(";");
         
         for item in ds_details:
            if item[:5] == "USER=":
               ds_username = item[5:];
            if item[:9] == "INSTANCE=":
               ds_instance = item[9:];
               
         if username == ds_username and instance == ds_instance:
            ds_match = ds_name;
            break;
            
      if ds_match is not None:
         validity = arcpy.ValidateDataStoreItem(ags,"DATABASE",ds_match);
            
         if validity == "valid":
            arcpy.AddMessage("      SUCCESS.");
               
         else:
            arcpy.AddMessage("      ERROR, please check this SDE connection on AGS server.");
            arcpy.AddMessage("      Preexisting Data Store " + ds_match + " failed to validate.");
            int_bad += 1;
               
      else:
         lst_ds = arcpy.ListDataStoreItems(ags,"DATABASE");
         for ds in lst_ds:
            ds_name = ds[0];
            if ds_name == tmp_data_store:
               arcpy.RemoveDataStoreItem(
                   ags
                  ,"DATABASE"
                  ,tmp_data_store
               );
               
         temp_sde = arcpy.CreateScratchName(
             "DZ" + str(uuid.uuid4()).replace("-","")
            ,".sde"
            ,None
            ,arcpy.env.scratchFolder
         );
         
         with open(sde_file, 'rb') as f1: 
            with open(temp_sde, 'wb') as f2:
               f2.write(f1.read())
         
         arcpy.AddDataStoreItem(
             ags
            ,"DATABASE"
            ,tmp_data_store
            ,temp_sde
            ,temp_sde
         );
         
         validity = "unknown";
         lst_ds = arcpy.ListDataStoreItems(ags,"DATABASE");
         for ds in lst_ds:
            ds_name = ds[0];
            if ds_name == tmp_data_store:
               validity = "valid";
            
               arcpy.RemoveDataStoreItem(
                   ags
                  ,"DATABASE"
                  ,tmp_data_store
               );
               
         if validity == "valid":
            arcpy.AddMessage("      SUCCESS.");
               
         else:
            arcpy.AddMessage("      ERROR, please check this SDE connection on AGS server.");
            int_bad += 1;

#------------------------------------------------------------------------------
# Step 50
# Finalize Results
#------------------------------------------------------------------------------
arcpy.AddMessage(" ");

if int_bad == 0:
   arcpy.AddMessage("All checks successful."); 
else:
   arcpy.AddMessage("Checks failed with " + str(int_bad) + " bad results.");  

arcpy.AddMessage(" ");
