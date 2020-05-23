from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import FileResponse
from datetime import datetime
from dotenv import load_dotenv
import mysql.connector as mysql
import requests
import os
import json
import re
import random

CurrentUser = "NONE"
REST_SERVER = os.environ.get('REST_SERVER')
#REST_SERVER = 'http://100.83.41.208:5000'
#The port is 5001, use that to access the website
#You should run the init_db once after building and upping the files


def convert_to_dict(list):

    new_dict = {"Coord1": {"long":list[1], "lat":list[0]}, "Coord2": {"long":list[3], "lat":list[2]}, "Coord3": {"long":list[5], "lat":list[4]}}
    print(new_dict)
    return new_dict  

def convert_to_user_dict(list):

    new_dict = {"first_name": list[1], "last_name": list[2], "email": list[3]}
    print(new_dict)
    return new_dict 

def parse_req(req):
    str = req.text
    str = re.split("\(|\)|\),\(|, ", str)
    for char in str: 
      if (char == ",") or (char == ""): 
        str.remove(char)

    print(str)
    split_text = convert_to_dict(str)
    return split_text

def parse_user_req(req):
  
  split_text = re.split('[= &]', req.text)
  split_text = convert_to_user_dict(split_text)
  return split_text

def add_coord(info):
  load_dotenv('credentials.env')
  db_user = os.environ['MYSQL_USER']
  db_pass = os.environ['MYSQL_PASSWORD']
  db_name = os.environ['MYSQL_DATABASE']
  db_host = os.environ['MYSQL_HOST']
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()

  query = "insert into Coordinates (1_lat, 1_long, 2_lat, 2_long, 3_lat, 3_long) values (%s, %s, %s, %s, %s, %s)"
  values = (info['Coord1']["lat"],info['Coord1']["long"],info['Coord2']["lat"],info['Coord2']["long"],info['Coord3']["lat"],info['Coord3']["long"])
  cursor.execute(query, values)
  db.commit()
  #print("added user")
  #docker exec -it 140demodb mysql -uelon -p
  print("WORKED UP TO HERE")



def home_page(req):
  return render_to_response('pages/home_page.html', {}, request=req)

def submit_signup(req):
  info = parse_user_req(req)
  print(info)
  #Users = get_user_data(req)
  #for User in Users:
  #    if info['email'] == User['email']:
  #        return render_to_response('templates/signup.html', {'message':'Email already registered!'}, request=req)  
  load_dotenv('credentials.env')
  db_user = os.environ['MYSQL_USER']
  db_pass = os.environ['MYSQL_PASSWORD']
  db_name = os.environ['MYSQL_DATABASE']
  db_host = os.environ['MYSQL_HOST']
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  query = "insert into Users (first_name, last_name, email) values (%s, %s, %s)"
  values = (info['first_name'],info['last_name'],info['email'])
  cursor.execute(query, values)
  db.commit()
  #print("added user")
  #docker exec -it 140demodb mysql -uelon -p
  print("WORKED UP TO HERE")
  return render_to_response('pages/signup.html', {'message':'Registered Email! Look for more info soon'}, request=req)

def signup(req):
  return render_to_response('pages/signup.html', {}, request=req)

def about_us(req):
  return render_to_response('pages/about_us.html', {}, request=req)
  
def product_features(req):
  return render_to_response('pages/product_features.html', {}, request=req)

def pricing_model(req):
  return render_to_response('pages/pricing_model.html', {}, request=req)

def planner(req):
  return render_to_response('pages/planner.html', {}, request=req)

def metrics(req):
  return render_to_response('pages/metrics.html', {}, request=req)

def check_status(req):  #Insert functions to eventually add this information
  return {"Status": "Ready", "Trip_time": "CALCULATED TIME", "Battery": "100%"}

def launch_command(req):
  #THIS IS WHERE YOU GET THE COORDINATES THAT THE DRONE WANTS TO GO
  print(req.text)
  split_text = parse_req(req)
  add_coord(split_text)
  return {"Status": "Ready", "Trip_time": "CALCULATED TIME", "Battery": "100%"}

def get_progress(req):
  cat = get_db("Select * from Progress;")
  print(cat)

  progress = {'Frontend': cat[0][1],'Backend':cat[0][2] ,'Hardware':cat[0][3] ,'Business':cat[0][4]}
  return progress

def get_count(req):
  cat = get_db("SELECT COUNT(*) FROM Users;")
  count = {'count': cat[0]}
  print(count)

  return count

def get_news(req):
  count = get_db("SELECT COUNT(*) from News;")
  cat = get_db("select * from News;")
  print(cat)
  new_dict = {"1": cat[0][1], "1_body": cat[0][2], "2": cat[1][1], "2_body": cat[1][2], "3": cat[2][1], "3_body": cat[2][2], "4": cat[3][1], "4_body": cat[3][2]}
  
  print(new_dict)
  return new_dict

def get_db(string_command):
    load_dotenv('credentials.env')
    db_user = os.environ['MYSQL_USER']
    db_pass = os.environ['MYSQL_PASSWORD']
    db_name = os.environ['MYSQL_DATABASE']
    db_host = os.environ['MYSQL_HOST']
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    cursor.execute(string_command)
    allrows = cursor.fetchall()        
    print(allrows)
    return allrows


if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

###############################


  config.add_route('home_page', '/')
  config.add_view(home_page, route_name='home_page') #first_page

  config.add_route('submit_signup', '/submit_signup')
  config.add_view(submit_signup, route_name='submit_signup')

  config.add_route('signup', '/signup')
  config.add_view(signup, route_name='signup')

  config.add_route('about_us', '/about_us')
  config.add_view(about_us, route_name='about_us') 

  config.add_route('product_features', '/product_features')
  config.add_view(product_features, route_name='product_features') 

  config.add_route('pricing_model', '/pricing_model')
  config.add_view(pricing_model, route_name='pricing_model') 

  config.add_route('planner', '/planner')
  config.add_view(planner, route_name='planner') 
  
  config.add_route('metrics', '/metrics')
  config.add_view(metrics, route_name='metrics')

  config.add_route('check_status', '/check_status')
  config.add_view(check_status, route_name='check_status', renderer="json") 

  config.add_route('launch_command', '/launch_command')
  config.add_view(launch_command, route_name='launch_command', renderer="json") 

  config.add_route('get_progress', '/get_progress')
  config.add_view(get_progress, route_name='get_progress', renderer="json")

  config.add_route('get_count', '/get_count')
  config.add_view(get_count, route_name='get_count', renderer="json")

  config.add_route('get_news', '/get_news')
  config.add_view(get_news, route_name='get_news', renderer="json")




#           AIzaSyBmdR6qGw3xWKJoqo1LviAVgl50sTcWfBA api key for google maps
#########################################


  config.add_static_view(name='/', path='./pages/CSS', cache_max_age=3600) #expose the CSS file
  
  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()


#Use firewatch_db
#select * from Users;