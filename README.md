thisremindsmeofthat
===================

This reminds me of that is a non-linear notebook that allows users not only to create and search through thoughts but also to create links between thoughts. 

I want to create a notebook that works more naturally with the way that my mind works. 

I love making assocations between things.  The more disparate the better.  I often think metaphorically. 

I wish there was a way to accumulate those associations.  I wonder if they would grow into something larger.  What if a strange connection between x and y could, months later, be easily accessible and connected to a new insight about z. 

I've made several attempts at scratching this itch over the past few years. The most recent version has been working well for me for several months. 

In particular I am pleased with the simplicity of my most recent approach. The entire thing is just a big (poorly written!) bash script that writes the thoughts and tracks the links among them in a text file. No database. No major setup. 

For these reasons, the current script file is called "trmt6.sh" but I'll probably adjust that now that I've gone fancy and put this on github.

Current explainer video: https://www.youtube.com/watch?v=N0jJYqTjVfY&t=1s


using thisremindsmeofthat
=========================

Core stuff:
-----------

Once you run the trmt script type add, followed by a thought to add that thought to the notebook. 
For example:  add This is my new thought. 

Use add to create thoughts as they come to you. 

Later if you want to search your thoughts. Just type search followed by one or more keywords.
For exmaple:  search antifragile

Now comes the fun part. As you search and create thoughts, pointers to those thoughts are written into an index file. This allows you to refer to thoughts and, critically, to make links between them. 

For example if your search turns up two or more thoughts, you will see them enumerated as s1, s2, s3... sn on the screen. If you wanted to link s1 to s2 then you type "link s1 s2"

Now thought s1 points to s2!

Sometimes handing thoughts requires more than one search, or you find you want to pin a thought in the index for later. To do that just type pin followed by the thought's id, followed by a location to pin it. (Starting with p)

For example, to pin the thought in search result 3 to slot 5 type "pin s3 p5"

Now you can do something like "link p5 s2" 

This'll make more sense after I record a video. I'll put a link to that here once I've got it on youtube.

But... ok now we have thoughts and links among those thoughts. Want to see the links? Then you need to go to a thought. 

So type something like "go p5" to go to the thought that you put in p5. When you do that it'll print out the thought and show you the inbound and outbound links to that thought. Inbound links are denoted with "b" and outbound links with "a". 

Meaning if you go to thought p5 and you see that it points to another interesting thought, you can type "go a1" to hop over to that thought. And so on!

Also for your reference, the most recent thought created is always in p0.

Other stuff:
------------

Have you cluttered up your pinned thoughts? No problem. Just type "nixpins" to clear them all out.

Looking for a thought you added recently? Type last followed by a number to get the last x thoughts. Example "last 5" for the last 5 thoughts.

Did you make a mistake? Use the merge option.

Merge allows you to take one thought and replace another with it. So if you type "merge p0 p5" then the end result will be that thought p5 goes away and all it's inbound and outbound links now reference p5 instead. (It's like p5 never existed...). Merge currently does the work you would expect out of merge, edit, and delete.

Do you want to maintain separate notebooks? No problem. By default trmt will add thoughts to a file called notebook.txt but you can say "setnotebook othernotebook.txt" and change that. "Othernotebook" can be whatever you want.

Portability:
------------
I've been writing the notebook and using it on my mac. I suspect I'm going to hit at least one snag when I move it over to my raspberry pi. I use md5 hashes for my thought ids. On a mac this seems to be just md5 but I think it might be slightly different on a real linux machine. 

Todo:
-----
Either follow through on adding endnotes to the code or take out the references to them.
Add random thoughts.
Add contemporaneous thoughts. 

Happy thinking!