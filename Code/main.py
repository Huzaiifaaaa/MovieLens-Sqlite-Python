import sqlite3
import objecttier

def commandOne(conn):
    command=input("\nEnter movie name (wildcards _ and % supported): ")
    movies=objecttier.get_movies(conn,command)
    movies=list(movies)

    print("\n# of movies found:",len(movies))

    if len(movies)>100:
        print("\nThere are too many movies to display, please narrow your search and try again...")
    else:
        print("\n\n")
        for i in range(len(movies)):
            print(str(movies[i].Movie_ID)+" : "+movies[i].Title+" ("+str(movies[i].Release_Year)+")")
    print("\n")

def commandTwo(conn):
    command=input("\nEnter movie id: ")
    moviedetails=objecttier.get_movie_details(conn,command)

    if moviedetails==None:
        print("\nNo such movie...")
    else:
        print("\n")
        print(str(moviedetails.Movie_ID)+" : "+moviedetails.Title)
        print("  Release date: "+str(moviedetails.Release_Date))
        print("  Runtime: "+str(moviedetails.Runtime)+" (mins)")
        print("  Orig language: "+moviedetails.Original_Language)
        print("  Budget: ${:,}".format(moviedetails.Budget)+" (USD)")
        print("  Revenue: ${:,}".format(moviedetails.Revenue)+" (USD)")
        print("  Num reviews: "+str(moviedetails.Num_Reviews))
        rating=str(float("{:.2f}".format(moviedetails.Avg_Rating)))
        if len(rating)==3:
            rating=rating+"0"
        print("  Avg rating: "+rating+" (0..10)")
        
        genre=', '.join(moviedetails.Genres)
        if moviedetails.Genres:
            print("  Genres: "+genre+", ")
        else:
            print("  Genres: "+genre)

        companies=', '.join(moviedetails.Production_Companies)
        if moviedetails.Production_Companies:
            print("  Production companies: "+companies+", ")
        else:
            print("  Production companies: "+companies)
        print("  Tagline: "+moviedetails.Tagline)

def commandThree(conn):
    N=input("\nN? ")
    if int(N)<=0:
        print("Please enter a positive value for N...")
        return
    
    num_of_reviews=input("min number of reviews? ")
    if int(num_of_reviews)<=0:
        print("Please enter a positive value for min number of reviews...")
        return

    topmovies=objecttier.get_top_N_movies(conn,int(N),int(num_of_reviews))
    if topmovies!=None:
        print("\n")
        for i in range(len(topmovies)):       
            reviews= str(float("{:.2f}".format(topmovies[i].Avg_Rating)))
            if len(reviews)==3:
                reviews=reviews+"0"

            print(str(topmovies[i].Movie_ID)+" : "+topmovies[i].Title+" ("+str(topmovies[i].Release_Year)+"), avg rating = "+str(reviews)+" ("+str(topmovies[i].Num_Reviews) +" reviews)")
        


def commandFour(conn):
    rating=input("\nEnter rating (0..10): ")
    if int(rating)<0 or int(rating)>10:
        print("Invalid rating...")
        return
    
    movieid=input("Enter movie id: ")
    output=objecttier.add_review(conn,int(movieid),int(rating))
    if output==0:
        print("\nNo such movie...")
    else:
        print("\nReview successfully inserted")
        


def commandFive(conn):
    tagline=input("\ntagline? ")
    movieid=input("movie id? ")

    output=objecttier.set_tagline(conn,int(movieid),tagline)
    if output==0:
        print("\nNo such movie...")
    else:
        print("\nTagline successfully set")



#create db connection
connection = sqlite3.connect('MovieLens.db')

print("** Welcome to the MovieLens app **\n")
print("General stats:")
print("  # of movies: {:,}".format(objecttier.num_movies(connection)))
print("  # of reviews: {:,}".format(objecttier.num_reviews(connection)))

while True:
    command=input("\nPlease enter a command (1-5, x to exit): ")

    if command=="1":
        commandOne(connection)
    elif command=="2":
        commandTwo(connection)
    elif command=="3":
        commandThree(connection)
    elif command=="4":
        commandFour(connection)
    elif command=="5":
        commandFive(connection)
    elif command=="x":
        exit()


