#　-*- coding: utf-8 -*-
import logging
import os
import webapp2
from google.appengine.ext.webapp import template
from src import main

class MainHandler(webapp2.RequestHandler):
    """
    /
    """
    def __init__(self, *args, **kwargs):
        #基底クラスの__init__()を呼ぶ
        super(MainHandler, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        logging.debug("query_string=" + self.request.query_string)
        logging.debug(kwargs)
        logging.debug(args)
        
        params = { 
                   }
        fpath = os.path.join(main.TEMPLATEPATH, "sample.html")
        html = template.render(fpath, params)
        self.response.out.write(html)
