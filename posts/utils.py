import datetime
import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
	#html_string = """ <h2> This is a title </h2> """
	word_string = strip_tags(html_string)
	matching_words = re.findall(r'\w+', word_string)
	count = len(matching_words)
	return count

def get_read_time(html_string):
	count = count_words(html_string)
	read_time_min = math.ceil(count/200.0) #using 200wpm for an average reader
	#read_time_sec = read_time_min * 60
	#read_time = str(datetime.timedelta(seconds=read_time_sec))
	read_time = str(datetime.timedelta(minutes=read_time_min))
	return read_time