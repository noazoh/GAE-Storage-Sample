#　-*- coding: utf-8 -*-
import logging
import os
import urllib
import webapp2
from src import main
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template

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
        
        #default bucket name
        from google.appengine.api import app_identity
        logging.debug("default bucket name=" + app_identity.get_default_gcs_bucket_name())

        #upload用URLを生成
        #アップロードが完了したら/uploadに遷移する
        upload_url = blobstore.create_upload_url('/upload', gs_bucket_name='noazoh-sandbox.appspot.com')
        logging.debug("upload_url=" + upload_url)

        # 現在 Blobstore に保存されているファイルたちを取得
        files = blobstore.BlobInfo.all()
        
        params = { 
                  "upload_url": upload_url,
                  "files": files,
                   }
        fpath = os.path.join(main.TEMPLATEPATH, "index.html")
        html = template.render(fpath, params)
        self.response.out.write(html)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self, *args, **kwargs):        
        logging.debug("query_string=" + self.request.query_string)
        logging.debug(kwargs)
        logging.debug(args)

        # Blobstore にアップロードされたファイルの情報を取得
        files = self.get_uploads('file')
        if files:
            logging.debug("upload files:" + files)
        else:
            logging.debug(u"アップロードファイル情報なし")

        # ファイル表示用の URL へリダイレクト
        # self.redirect('/serve/%s' % blob_info.key())


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, blob_key):
        logging.debug("blob_key:" + blob_key)
        blob_key = str(urllib.unquote(blob_key)) 

        # BlobKeyを指定してファイルを取得
        blob_info = blobstore.BlobInfo.get(blob_key)

        # 結果をクライアントに返す
        self.send_blob(blob_info)


class DownloadHandler(webapp2.RequestHandler):
    """
    /download 
    """
    def post(self, *args, **kwargs):
        logging.debug("query_string=" + self.request.query_string)
        logging.debug(kwargs)
        logging.debug(args)
    
    