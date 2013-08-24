thisremindsmeofthat
===================

Neo4j based associative notebook

I want to create a notebook that works more naturally with the way that my mind works. 

I love making assocations between things.  The more disparate the better.  I often think metaphorically. 

I wish there was a way to accumulate those associations.  I wonder if they would grow into something larger.  What if a strange connection between x and y could, months later, be easily accessible and connected to a new insight about z. 

I got introduced to Neo4j a couple months ago.  It seems like the perfect foundation for building this associative notebook.  I've played with this idea before, along with my friend Chris. I've never been quite able to bring the idea to life. I think with Neo4j I can.  A graph database already does what I've dreamed about doing. Now it's a matter of working out an intuitive way to add a note node to the graph and discover relationships between it and previous nodes. 

Since I'm not good at writing code this will be easier said than done.

===================
Data Modeling

Each node in this app will represent a "this" node.  As in the this in thisremindsmeofthat. A this node has three properties: text (140 characters representing the substance of the node), a create date and a modified date.

Each relationship in the app will be a "reminds me of" rel. A relationship will have three properties: link (140 characters representing the reason for the connection), a create date and a modified date.

