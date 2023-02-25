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
        print("  Avg rating: "+str(moviedetails.Avg_Rating)+"0 (0..10)")
        
        genre=', '.join(moviedetails.Genres)
        if moviedetails.Genres:
            print("  Genres: "+genre+",")
        else:
            print("  Genres: "+genre)

        companies=', '.join(moviedetails.Production_Companies)
        if moviedetails.Production_Companies:
            print("  Production companies: "+companies+",")
        else:
            print("  Production companies: "+companies)
        print("  Tagline: "+moviedetails.Tagline)

def commandThree(conn):
    pass

def commandFour(conn):
    pass

def commandFive(conn):
    pass



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


