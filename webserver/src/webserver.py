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
    new_dict = {list[i]: list[i + 1] for i in range(0, len(list), 2)}
    return new_dict  

def parse_req(req):
    split_text = re.split('[= &]', req.text)
    split_text = convert_to_dict(split_text)
    return split_text

def home_page(req):
  return render_to_response('pages/home_page.html', {}, request=req)

def submit_signup(req):
  info = parse_req(req)
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
  config.add_view(about_us, route_name='about_us') #first_page

  config.add_route('product_features', '/product_features')
  config.add_view(product_features, route_name='product_features') #first_page

  config.add_route('pricing_model', '/pricing_model')
  config.add_view(pricing_model, route_name='pricing_model') #first_page

#           AIzaSyBmdR6qGw3xWKJoqo1LviAVgl50sTcWfBA api key for google maps
#########################################


  config.add_static_view(name='/', path='./pages/CSS', cache_max_age=3600) #expose the CSS file
  
  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()

