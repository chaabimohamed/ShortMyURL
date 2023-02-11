# ShortMyURL
ShortMyURL is a straightforward restful API that allows clients to create short links.

Users,URLS
* General
	- user have token for 3 day if the token
* Table user (id,username,email,password,isadmin)
	- client can create new user if isadmin=true/update information of a user/ delete user
	- client can change there username or password using email verification
* Table URL (id,basURL,newURL,userid)
	- client can add new URL / delete/update ... (if he has a authentification)
	- admin can remove any URL