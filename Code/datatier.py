#
# datatier.py
#
# Executes SQL queries against the given database.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project 02
#
import sqlite3


##################################################################
#
# select_one_row:
#
# Given a database connection and a SQL Select query,
# executes this query against the database and returns
# the first row retrieved by the query (or the empty
# tuple () if no data was retrieved). The query can
# be parameterized, in which case pass the values as
# a list via parameters; this parameter is optional.
#
# Returns: first row retrieved by the given query, or
#          () if no data was retrieved. If an error
#          occurs, a msg is output and None is returned.
#
# NOTE: error message format is 
#   print("select_one_row failed:", err)
# where err is the Exception object.
#
def select_one_row(dbConn, sql, parameters=None):
   #try to execute query
   try:
      # create a cursor object:
      cursor = dbConn.cursor()

      if parameters:#if parameter not null
         cursor.execute(sql, parameters)#execute query with parameters
      else:#if parameters is null, execute query
         cursor.execute(sql)#execute query

      #fetch result, get onpy 1 row/result   
      row = cursor.fetchone()

      #if null, return empty tuple
      if row is None:
         return ()
      else:
         return row#return row

   #if error, print error message(catch exceptions)
   except Exception as err:
      print("select_one_row failed:", err)#print message
      return None#return none



##################################################################
#
# select_n_rows:
#
# Given a database connection and a SQL Select query,
# executes this query against the database and returns
# a list of rows retrieved by the query. If the query
# retrieves no data, the empty list [] is returned.
# The query can be parameterized, in which case pass 
# the values as a list via parameters; this parameter 
# is optional.
#
# Returns: a list of 0 or more rows retrieved by the 
#          given query; if an error occurs a msg is 
#          output and None is returned.
#
# NOTE: error message format is 
#   print("select_n_rows failed:", err)
# where err is the Exception object.
#
def select_n_rows(dbConn, sql, parameters=None):
   #try to execute query
   try:
      # create a cursor object
      cursor = dbConn.cursor()

      if parameters:#if parameter not null
         cursor.execute(sql, parameters)#execute query with parameters
      else:#if parameters is null, execute query
         cursor.execute(sql)#execute query

      rows = cursor.fetchall()#fetch all results, gets multiple results/rows
      return rows#return rows

   #catch exceptions, if any   
   except Exception as err:
      print("select_n_rows failed:", err)#print error message
      return None#return None



##################################################################
#
# perform_action: 
# 
# Given a database connection and a SQL action query,
# executes this query and returns the # of rows
# modified; a return value of 0 means no rows were
# updated. Action queries are typically "insert", 
# "update", "delete". The query can be parameterized,
# in which case pass the values as a list via 
# parameters; this parameter is optional.
#
# Returns: the # of rows modified by the query; if an 
#          error occurs a msg is output and -1 is 
#          returned. Note that a return value of 0 is
#          not considered an error --- it means the
#          query did not change the database (e.g. 
#          because the where condition was false?).
#
# NOTE: error message format is 
#   print("perform_action failed:", err)
# where err is the Exception object.
#
def perform_action(dbConn, sql, parameters=None):
   #try to execute query
   try:
      # create a cursor object
      cursor = dbConn.cursor()

      if parameters:#if parameter not null
         cursor.execute(sql, parameters)#execute query with parameters
      else:#if parameters is null, execute query
         cursor.execute(sql)#execute query

      count = cursor.rowcount#count number of rows affected
      dbConn.commit()#commit changes
      return count#return count

   #catch exceptions, if any   
   except Exception as err:
      dbConn.rollback()#roll back changes to orignal state
      print("perform_action failed:", err)#print error message
      return -1#return error code -1

