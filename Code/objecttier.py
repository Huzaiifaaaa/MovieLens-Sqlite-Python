# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
   def __init__(self, movie_id, title, release_year):
      self._Movie_ID = movie_id
      self._Title = title
      self._Release_Year = release_year

   @property
   def Movie_ID(self):
      return self._Movie_ID

   @property
   def Title(self):
      return self._Title
   
   @property
   def Release_Year(self):
      return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
   def __init__(self, movie_id, title, release_year, num_reviews, avg_rating):
      self._Movie_ID = movie_id
      self._Title = title
      self._Release_Year = release_year
      self._Num_Reviews = num_reviews
      self._Avg_Rating = avg_rating

   @property
   def Movie_ID(self):
      return self._Movie_ID
   
   @property
   def Title(self):
      return self._Title

   @property
   def Release_Year(self):
      return self._Release_Year
   
   @property
   def Num_Reviews(self):
      return self._Num_Reviews

   @property
   def Avg_Rating(self):
      return self._Avg_Rating





##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
   def __init__(self, movie_id, title, release_date, runtime, original_language, budget, revenue, num_reviews, avg_rating, tagline, genres, production_companies):
      self._Movie_ID = movie_id
      self._Title = title
      self._Release_Date = release_date
      self._Runtime = runtime
      self._Original_Language = original_language
      self._Budget = budget
      self._Revenue = revenue
      self._Num_Reviews = num_reviews
      self._Avg_Rating = avg_rating
      self._Tagline = tagline
      self._Genres = genres
      self._Production_Companies = production_companies

   @property
   def Movie_ID(self):
      return self._Movie_ID

   @property
   def Title(self):
      return self._Title
   
   @property
   def Release_Date(self):
      return self._Release_Date
   
   @property
   def Runtime(self):
      return self._Runtime

   @property
   def Original_Language(self):
      return self._Original_Language

   @property
   def Budget(self):
      return self._Budget

   @property
   def Revenue(self):
      return self._Revenue

   @property
   def Num_Reviews(self):
      return self._Num_Reviews

   @property
   def Avg_Rating(self):
      return self._Avg_Rating

   @property
   def Tagline(self):
      return self._Tagline

   @property
   def Genres(self):
      return self._Genres

   @property
   def Production_Companies(self):
      return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
   try:
      query="SELECT COUNT(*) FROM Movies"
      row=datatier.select_one_row(dbConn, query)
      return int(row[0])
   except:
      return -1



##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
   try:
      query="SELECT COUNT(*) FROM Ratings"
      row=datatier.select_one_row(dbConn, query)
      return int(row[0])
   except:
      return -1


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
   try:
      query="SELECT * FROM Movies WHERE Title LIKE ? ORDER BY Movie_ID"
      rows=datatier.select_n_rows(dbConn, query, (pattern,))
      movies=[]
      for row in rows:
         year=row[1].split('-')[0]
         movie = Movie(row[0], row[6], year)
         movies.append(movie)
      return movies
   except:
      return []



##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
   try:

      moviedata=datatier.select_one_row(dbConn, "SELECT * FROM Movies WHERE Movie_ID = ? ORDER BY Movie_ID", (movie_id,))
      moviedata=list(moviedata)

      if moviedata:
         reviews=datatier.select_one_row(dbConn, "SELECT COUNT(*), SUM(Rating) FROM Ratings WHERE Movie_ID = ?", (movie_id,))
         tagline=datatier.select_one_row(dbConn, "SELECT Tagline FROM Movie_Taglines WHERE Movie_ID = ?", (movie_id,))

         genreids=datatier.select_n_rows(dbConn, "SELECT Genre_ID FROM Movie_Genres WHERE Movie_ID = ? ORDER BY Genre_ID", (movie_id,))
         genrelist=[]
         for genreid in genreids:
            genre=datatier.select_one_row(dbConn, "SELECT Genre_Name FROM Genres WHERE Genre_ID=?", (int(genreid[0]),))
            genrelist.append(genre[0])

         companynames=datatier.select_n_rows(dbConn, "SELECT Company_ID from Movie_Production_Companies WHERE Movie_ID = ? ORDER BY Company_ID", (movie_id,))
         companylist=[]
         for company in companynames:
            company=datatier.select_one_row(dbConn, "SELECT Company_Name FROM Companies WHERE Company_ID=?", (int(company[0]),))
            companylist.append(company[0])

         genrelist.sort()
         companylist.sort()
         reviews=list(reviews)

         if reviews[0] != 0:
            reviews[1]=reviews[1]/reviews[0]
         else:
            reviews[1]=0

         tagline=list(tagline)
         
         tag=""
         if tagline:
            tag=tagline[0]

         movie_details = MovieDetails(moviedata[0], moviedata[6], moviedata[1].split(' ')[0], moviedata[2], moviedata[3], moviedata[4], moviedata[5],reviews[0],reviews[1], tag, genrelist, companylist)
         return movie_details
      else:
         return None
   except:
      traceback.print_exc()
      return None

         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
   try:
      #movie_id, title, release_year, num_reviews, avg_rating)

      #join movies with ratings
      query="SELECT Movies.Movie_ID, Movies.Title, Movies.release_date, COUNT(*), AVG(Rating) FROM Movies INNER JOIN Ratings ON Movies.Movie_ID = Ratings.Movie_ID WHERE Rating > 0 GROUP BY Movies.Movie_ID HAVING COUNT(*) >= ? ORDER BY AVG(Rating) DESC"
      moviedata=datatier.select_n_rows(dbConn, query, (min_num_reviews,))
      
      movieratings=[]
      count=0
      for i in range(len(moviedata)):
         if moviedata[i][1]!="":
            movieratings.append(MovieRating(moviedata[i][0], moviedata[i][1], moviedata[i][2].split('-')[0], moviedata[i][3], moviedata[i][4]))
            count=count+1
         
         if count==N:
            break

      return movieratings
   except:
      traceback.print_exc()
      return []



##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
   try:
      moviedata=datatier.select_one_row(dbConn, "SELECT * FROM Movies WHERE Movie_ID = ? ORDER BY Movie_ID", (movie_id,))
      moviedata=list(moviedata)

      if moviedata:
         query="INSERT INTO Ratings (Movie_ID, Rating) VALUES (?, ?)"
         datatier.perform_action(dbConn, query, (movie_id, rating))
         return 1
      else:
         return 0
   except:
      return 0


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
   try:
      # Check if the movie exists in the database
      movie=datatier.select_one_row(dbConn, "SELECT * FROM Movies WHERE Movie_ID = ?", (movie_id,))
      
      if movie:
         # Check if the movie already has a tagline
         tag=datatier.select_one_row(dbConn, "SELECT Tagline FROM Movie_Taglines WHERE Movie_ID = ?", (movie_id,))
         tag=list(tag)
         
         # If the movie already has a tagline, update it
         if tag:
            count=datatier.perform_action(dbConn, "UPDATE Movie_Taglines SET tagline=? WHERE Movie_ID=?", (tagline, movie_id))
         else:
            count=datatier.perform_action(dbConn, "INSERT INTO Movie_Taglines (Movie_ID, Tagline) VALUES (?, ?)", (movie_id, tagline))         
         return 1
      else:
         return 0
   except:
      return 0

   

