# bookclub_portfolio

Django/postgres backend application to track book recommendations by members of the book club.

Database Tables

Books
	id		    Serial
	title		Text	
	author		Text
	genre		Text

Members
	id		    Serial
	name		Text	
	email		Text

Recommendations
	id		    Serial
	book        Foreign Key(Books)
	member	    Foreign Key(Members)
	r_date	    Date


Endpoints


api/book/		        	POST, GET, DELETE   - JSON request body can optionally be used for filtering in GET
                                                	valid keys: title, author, and genre
api/book/<id>/	        	GET, PUT, DELETE    
api/member/		        	POST, GET, DELETE   - JSON request body can optionally be used for filtering in GET
                                                	valid keys:  name and email
api/member/<id>	        	GET, PUT, DELETE    
api/recommendation/	    	POST, GET, DELETE   - JSON request body can optionally be used for filtering in GET
                                                	valid keys: name, title, author, genre, r_date
api/recommendation/<id>/    DELETE
api/recommmendation/latest/	GET                                        