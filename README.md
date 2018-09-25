# Manipulating KNX Telegrams
 
  > A tool to read telegrams from our KNX-Log-Database, change individual properties and write back the altered telegram to the Log-Database.
  
Changes of individual parameters within one database record must also be reflected within the cemi field of that same record. 

Consistency check is required, since the database itself is purely designed - it holds redundant data.
Besides the information encoded within the entire cemi, most properties are listed again seperately. This is done so that research with the data becomes more easy, allowing for quicker understanding and human readability.

## Installation

In your Python virtual environment use
  > pip install -r requirements.txt
