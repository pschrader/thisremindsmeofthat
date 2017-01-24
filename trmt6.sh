#!/bin/bash


##########################################
#                                        #
# Configuration                          #
#                                        # 
##########################################

#set the notebook file
notebook=notebook.txt

#delete the index if it exists
rm index.txt

#recreate the index file
touch index.txt

##########################################
#                                        #
# Function Library                       #
#                                        # 
##########################################


### The Set Notebook function changes the file you are logging notes in  ###
### See endnote x for more info		       	                         ###
setnotebook ()
{

	#delete the index if it exists
	rm index.txt

	#recreate the index file
	touch index.txt
	
	#set the notebook file
	notebook=$2
	clear
	echo "Notebook set to $notebook"
}

### The Link function adds a link between two thoughts  ###
### See endnote x for more info		       	        ###
link ()
{
	clear

	#Check for args
	if [ $# -lt 3 ]
	then
		clear
		echo "No link. Need a second thought to link to"
		main
	fi	

	#Link thought A to B
	
	#Get A's ID
	index_a=$2
	index_a+=:
	trimmer=${#index_a}
	((trimmer+=1))
	id_a=$(egrep -o "^$index_a.{32}" index.txt | cut -c ${trimmer}-)

	#Get B's ID
	index_b=$3
	index_b+=:
	trimmer=${#index_b}
	((trimmer+=1))
	id_b=$(egrep -o "^$index_b.{32}" index.txt | cut -c ${trimmer}-)

	#Check if you are trying to link the thought to itself
	if [ "$id_a" == "$id_b" ]
	then
		echo "No link. Can't link a thought to itself."
	#check if the two thoughts are already linked
	elif grep "^$id_a" $notebook | grep -q "|.*$id_b"
	then
		echo "No Link. Already linked."
	else
	#add the link
		sed -i.bak "/^$id_a/ s/$/$id_b;/" $notebook
		echo "Link created"
		#go to id_a
	fi
	
}

### The Unlink function removes the link between two thoughts   ###
### See endnote x for more info				        ###
unlink ()
{
	clear

	#Get A's ID
	index_a=$2
	index_a+=:
	trimmer=${#index_a}
	((trimmer+=1))
	id_a=$(egrep -o "^$index_a.{32}" index.txt | cut -c ${trimmer}-)

	#Get B's ID
	index_b=$3
	index_b+=:
	trimmer=${#index_b}
	((trimmer+=1))
	id_b=$(egrep -o "^$index_b.{32}" index.txt | cut -c ${trimmer}-)

	#remove the link
	sed -i.bak "/^$id_a/ s/$id_b;//" $notebook
	echo "Thoughts Unlinked (assuming they were linked in the first place)"
}

### The Add function adds new thoughts to the notebook file ###
### See endnote x for more info				    ###
add ()
{
	clear
	phrase=${1#"add "}
	md5thought=$(md5 <<< $phrase)
	echo "$md5thought|$phrase|$(date +"%Y-%m-%d_%H-%M-%S")|" >> $notebook

	#Now display the thought
	echo Added $phrase

	#Now update the index file - p0 entry
	sed /^p0/d index.txt > tempindex.txt
	mv tempindex.txt index.txt
	echo "p0:$md5thought|$phrase|$(date +"%Y-%m-%d_%H-%M-%S")|" >> index.txt
	sort index.txt -o index.txt

	#Future: add a recents entry to index.txt
}


### The Search function searches the notebook for a keyword    ###
### See endnote x for more info				       ###
search ()
{
	#First remove the existing search lines from the index
	sed /^s[0-9]/d index.txt > tempindex.txt
	mv tempindex.txt index.txt
	keywords=${1#"search "}
	ticker=1
	clear
	echo Search results for $keywords
	printf "\n"
	grep -i "$keywords" $notebook \
	| while read -r line ; do
		result=$(echo $line | grep -o '|.*|' | sed 's/|/  /g')
		
		#get id of thie line and count links
		search_id=$(echo $line | cut -c -32)
		in_links=$(grep -c "$search_id" $notebook)
		in_links=$((in_links-1))
		out_links=$(echo $line | rev | egrep -o ";.{32}" | grep -c '')
		link_count=$((in_links + out_links))	

		printf "s$ticker: $result[$link_count]\n\n" | fold -s
		

		echo "s$ticker:$line" | grep -o '.*|.*|' >> index.txt
		ticker=$((ticker+1))
		done
}


### The Nixpins function removes the pointsers form  index   ###
### See endnote x for more info				     ###
nixpins ()
{
	clear
	sed /^p[0-9]/d index.txt > tempindex.txt
	mv tempindex.txt index.txt
	echo "Pins nix'd from index"
}


### The Pin function adds a pointer to index	 	    ###
### See endnote x for more info				    ###
pin ()
{
	clear
	grep "^$2" index.txt | sed "s/^$2/$3/" >> index.txt
	sort index.txt -o index.txt
	echo "Thought pinned to $3"
}


### The Pins function lists the pointers in index 	    ###
### See endnote x for more info				    ###
pins ()
{
	clear
	grep '^p' index.txt | sed -e 's/:................................/ /' | \
		rev | cut -c 2- | rev | sed 's/|/  /g'

}


### The Go function lists a thought and shows its related thoughts    ###
### See endnote x for more info				              ###
go ()
{
	clear

	#nix any "go lines" in the index
	sed /^g[0-9]/d index.txt > tempindex.txt
	mv tempindex.txt index.txt

	#add a g1 pointer to index
	go_line=$(grep "^$2:" index.txt | sed "s/^$2:/g0:/")
	echo $go_line >> index.txt
	echo "here"

	#display the thought at the top of the screen
	chop_line=$(grep "^$2:" index.txt | grep -o '|.*|.*|' | \
		cut -c 2- | rev | cut -c 2- | rev)
	thought=$(echo $chop_line | grep -o '^.*|' | rev | cut -c 2- | rev)
	timestamp=$(echo $chop_line | grep -o '|.*$' | cut -c 2-)
	echo $timestamp
	printf "\n\t$thought\n\n" | fold -s

	#get the id of the thought from the index file
	index_go=$2
	index_go+=:
	trimmer=${#index_go}
	((trimmer+=1))
	id_go=$(egrep -o "^$index_go.{32}" index.txt | cut -c ${trimmer}-)
	#echo $id_go
	
	#nix any "link lines" in the index
	sed /^[ab][0-9]/d index.txt > tempindex.txt
	mv tempindex.txt index.txt
	
	#spit out the inbound links (backlinks)
	ticker=1
	
	if grep -q "|.*|.*$id_go" $notebook
	then
		echo "--- Inbound References ---"
	fi

	grep "|.*|.*$id_go" $notebook \
		| while read -r line ; do
		
			#stick the link into index
			echo b$ticker:$line >> index.txt
		
			#parse elements and print the link
			bref_chop=$(echo $line | grep -o '|.*|.*|' | \
				cut -c 2- | rev | cut -c 2- | rev)
			bref_text=$(echo $bref_chop | grep -o '^.*|' | \
				rev | cut -c 2- | rev)
			bref_stamp=$(echo $bref_chop | grep -o '|.*$' | \
				cut -c 2-)
				
			#get id and check for number of links
			bref_id=$(echo $line | cut -c -32)
			in_links=$(grep -c "$bref_id" $notebook)
			in_links=$((in_links-1))
			out_links=$(echo $line | rev | egrep -o ";.{32}" | grep -c '')
			link_count=$((in_links + out_links))	
			
			printf "b$ticker: $bref_text\n\t$bref_stamp\t[$link_count]\n\n" | fold -s
			
		ticker=$((ticker+1))
		done

	#spit out the outbound links
	ticker=1
	if grep "^$id_go" $notebook | rev | grep -q "^;"
	then
		echo "--- Outbound References ---"
	fi
	grep "^$id_go" $notebook | rev | egrep -o ";.{32}" | cut -c 2- | rev |\
		while read -r line ; do
			
			#stick the link into index
			link=$(grep "^$line" $notebook)
			echo a$ticker:$link >> index.txt
	
			#parse elements and print the link
			href_chop=$(echo $link | grep -o '|.*|.*|' | \
				cut -c 2- | rev | cut -c 2- | rev)
			href_text=$(echo $href_chop | grep -o '^.*|' | \
				rev | cut -c 2- | rev)
			href_stamp=$(echo $href_chop | grep -o '|.*$' | \
				cut -c 2-)
			
			#get id and check for number of links
			href_id=$(echo $link | cut -c -32)
			in_links=$(grep -c "$href_id" $notebook)
			in_links=$((in_links-1)) 
			out_links=$(echo $link | rev | egrep -o ";.{32}" | grep -c '')			
			link_count=$((in_links + out_links))

			printf "a$ticker: $href_text\n\t$href_stamp\t[$link_count]\n\n" | fold -s

			ticker=$((ticker+1))
			done	

}


### The Merge function merges two thoughts together                                  ###
### The first thought consumes the second, taking on it's outbound and inbound links ###
### Merge can also be used for editing and overwriting thoughts with new ones        ###
### See endnote x for more info				                             ###

merge ()
{
	clear

	#get the id of the note that will be kept
	index_keep=$2
	index_keep+=:
	trimmer=${#index_keep}
	((trimmer+=1))
	id_keep=$(egrep -o "^$index_keep.{32}" index.txt | cut -c ${trimmer}-)
	#echo $id_keep

	#get the id of the note that will be devoured
	index_nix=$3
	index_nix+=:
	trimmer=${#index_nix}
	((trimmer+=1))
	id_nix=$(egrep -o "^$index_nix.{32}" index.txt | cut -c ${trimmer}-)
	#echo $id_nix

	#unlink keep from nix if they are linked
	sed -i.bak "/^$id_keep/ s/$id_nix;//" $notebook
	
	#get nix's outbound links
	#so they can be given to keep

	#we'll store them in a file called holdlinks.temp
	#so first we'll clear that file out
	touch holdlinks.temp
	rm holdlinks.temp
	touch holdlinks.temp

	grep "^$id_nix" $notebook | rev | egrep -o ";.{32}" | cut -c 2- | rev |\
		while read -r line ; do
			echo $line >> holdlinks.temp
			done	
	
	#get keep's outbound links and remove duplicates from holdlinks.temp
	grep "^$id_keep" $notebook | rev | egrep -o ";.{32}" | cut -c 2- | rev |\
		while read -r line ; do
			sed -i.bak "/$line/d" holdlinks.temp
			done	

	#take keep id out of holdlinks.temp
	#you don't want a thought to be linked to itself after the merge
	sed -i.bak "/$id_keep/d" holdlinks.temp

	#echo "hold links"
	#cat holdlinks.temp
	cat holdlinks.temp |\
		while read -r line ; do
			sed -i.bak "/^$id_keep/ s/$/$line;/" $notebook
			done

	#now delete the nix line	
	sed -i.bak "/^$id_nix/d" $notebook

	#and replace all the remaining nix ids with keep ids
	#sorry nix, it's like you never existed...
	sed -i.bak "s/$id_nix/$id_keep/g" $notebook

}

##########################################
#                                        #
# Main:                                  #
# Process the user command and run it    #
#                                        # 
##########################################

main ()
{
	printf "\n\n"
	echo ------------------------------
	echo -n "$notebook:  "
	read command

	case $command in
		c		)	clear ;;
		add*		)	add "$command";;
		exit		)	exit 0 ;;
		search*		)	search "$command";;
		link*		)	link $command;;
		unlink*		)	unlink $command;;
		nixpins		)	nixpins ;;
		pins		)	pins ;;
		pin*		)	pin $command;;
		setnotebook*	)	setnotebook $command;;
		go*		)	go $command;;
		merge*		)	merge $command;;
		*		)	clear;echo "Unknown command: $command";
	esac
}

clear
while [ true ]
do
	main
done


##########################################
#                                        #
# Endnotes				 #
#                                        # 
##########################################

# add a recents ticker
# add a getid function
# add a get links function

