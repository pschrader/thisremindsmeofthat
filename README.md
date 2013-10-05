thisremindsmeofthat
===================

Neo4j based associative notebook using py2neo to interact with the database

I want to create a notebook that works more naturally with the way that my mind works. 

I love making assocations between things.  The more disparate the better.  I often think metaphorically. 

I wish there was a way to accumulate those associations.  I wonder if they would grow into something larger.  What if a strange connection between x and y could, months later, be easily accessible and connected to a new insight about z. 

I got introduced to Neo4j a couple months ago.  It seems like the perfect foundation for building this associative notebook. Plus, there's a way to interact with neo4j using python thanks to py2neo.

I've played with this idea before, along with my friend Chris. I've never been quite able to bring the idea to life. I think with Neo4j and py2neo I can.  A graph database already does what I've dreamed about doing. Now it's a matter of working out an intuitive way to add a note node to the graph and discover relationships between it and previous nodes. 

Since I'm not good at writing code this will be easier said than done.


How to install and run
======================

Install neo4j

Install py2neo

Clone thisremindsmeofthat repo

from the python client
```python
  from trmtCmdLine import *
  cmdLine()
  
  enter command: add "New thing that reminds me of another thing"
  ```
  
  
Using trmtCmdLine
=====================
trmtCmdLine is a python script that interprets command line style commands to interact with the neo4j database.  Here are some examples of using commands

--Add a Thought--
Add a thought using the "add" command followed by a quoted string that contains the text of the thought that you want to add.  Here is an example of adding a new thought where the text of the thought is "Thing A"

enter command:  add "Thing A"

--View All Thoughts--
View a list of thoughts using the "ls" command. This will return a list of all thoughts and the ids of those thoughts in the neo4j database

enter command:  ls

--Search For Thoughts--
Search for thoughts that contain a given keyword string using the "kwrd" command, followed by a quoted string that contains the keyword phrase you are searching for.  Here is an example of searching trmt for all the thoughts that contain the string "thing".  Keyword search is not case sensitive.

enter command:  kwrd "thing"

--Connecting Thoughts--
Connect two thoughts using the "trt" command, followed by the ids of the nodes you want to connect and a quoted string for the relationship type you want to create between those nodes.  (trt stands for "this reminds me of that").  Note, the command line interface relies heavily on internal ids in neo4j, which everyone tells me is poor practice.  

enter command:  trt 1 2 "REMINDS_ME_OF"

