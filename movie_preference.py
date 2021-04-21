import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
source1 = 'https://cdncontribute.geeksforgeeks.org/wp-content/uploads/file.tsv'
source2 = 'https://cdncontribute.geeksforgeeks.org/wp-content/uploads/Movie_Id_Titles.csv'

# create a basic DataFrame with movie_titles and informations
def basic_table():
	columns = ['user_id', 'item_id', 'rating', 'timestamp']
	frame_with_rating = pd.read_csv(source1, sep = '\t', names = columns)
	frame_with_title = pd.read_csv(source2)
	basic = pd.merge(frame_with_rating, frame_with_title, on = 'item_id')
	return basic

# create a DataFrame to show the means and the counts of ratings
def ratings_table(basic):
	ratings = pd.DataFrame(basic.groupby('title')['rating'].mean())
	ratings['num_rating'] = basic.groupby('title')['rating'].count()
	return ratings

# create a DataFrame with the correlation coefficient between movies
def similar(movie1, movie2, minimum_amount, basic, ratings, pn1, pn2):
	movie_mate = basic.pivot_table(index='user_id', columns='title', values='rating')
	movie_mate['control_group'] = ( (movie_mate[movie1]*pn1) + (movie_mate[movie2]*pn2) ) / 2
	corr_table = pd.DataFrame(movie_mate.corrwith(movie_mate['control_group']), columns=['Correlation'])
	corr_table.drop('control_group', inplace=True)
	final_table = corr_table[ratings['num_rating'] > minimum_amount].sort_values(by='Correlation', ascending=False)
	final_table.dropna(inplace=True)
	final_table.drop([movie1, movie2], inplace=True)
	print(final_table.head())

# creat some movies name to try the respository
def rnd_movie_list():
	import random
	rnds = [random.randint(0, 10) for _ in range(10)]
	movie_list = pd.read_csv(source2).loc[rnds ,'title']
	print(movie_list)

# to find a movie for a user who like(pn=1) or dislike(pn=0) the movies (movie1 & movie2)
def main(movie1, movie2, minimum_amount=100, pn1=1, pn2=1):
	basic = basic_table()
	ratings = ratings_table(basic)
	similar(movie1, movie2, minimum_amount, basic, ratings, pn1, pn2)

main('Star Wars (1977)', 'Toy Story (1995)')



