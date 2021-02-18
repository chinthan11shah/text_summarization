import pandas as pd
import newspaper
import datetime
from entity import entity_finder as ef
import sqlite3
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.python.ops.rnn_cell_impl import _zero_state_tensors
import re
from nltk.corpus import stopwords
import time
import csv
from sqlalchemy import create_engine


cnx = create_engine('sqlite:///Newspaper.db').connect()
telegraph = pd.read_sql_table('Telegraph',cnx)
ht = pd.read_sql_table('Hindustan_Times',cnx)
ie = pd.read_sql_table('Indian_Express',cnx)
fpj = pd.read_sql_table('FPJ',cnx)
frames = [telegraph,ht,ie,fpj]
df = pd.concat(frames)
df.head(5)
