import xmlrpclib
import time
import exceptions

class MSMetaWeblogException(exceptions.Exception):  
    def __init__(self, obj):
        if isinstance(obj, xmlrpclib.Fault):
            self.id = obj.faultCode
            self.message = obj.faultString
        else:
            self.id = 0
            self.message = obj

    def str(self):
        return '<%s %d: \'%s\'>' % ('MetaWblog Error:', self.id, self.message)
    
class UserBlog:
    def __init__(self):
        self.url=''
        self.blogID=''
        self.blogName=''
        
class UserInfo:
    def __init__(self):
        self.url=''
        self.userID=''
        self.firstName=''
        self.lastName=''
        self.email=''
        self.nickName=''

class Category:
    def __init__(self):
        self.description=''
        self.title=''

class NewPost:
    def __init__(self):
        self.description=''
        self.title=''        
        self.categories=[]
        
class Post:
    def __init__(self):
        self.dateCreated=None
        self.description=''
        self.title=''
        self.PostId=''
        self.categories=[]


class MsMetaBlogAPI:
    def __init__(self,blogID,userName,passWord):
        self.blogID=blogID
        self.userName=userName
        self.passWord=passWord
        self.url='https://storage.msn.com/storageservice/MetaWeblog.rpc'
        self._server=xmlrpclib.Server(self.url,allow_none=True)
    
    def _filterPost(self,post):
        postObject=Post()        
        
        postObject.dateCreated=time.strptime(str(post['dateCreated']), "%Y-%m-%dT%H:%M:%SZ")
        postObject.description=post['description']
        postObject.title=post['title']
        postObject.postID=post['postid']
        postObject.categories=post['categories']
        
        return postObject
    
    def _filterCategory(self,category):
        categoryObj=Category()
        
        categoryObj.description=category['description']
        categoryObj.title=category['title']
        
        return categoryObj
    
    def _filterUserBlog(self,userBlog):
        userBlogObj=UserBlog()
        
        userBlogObj.url=userBlog['url']
        userBlogObj.blogID=userBlog['blogid']
        userBlogObj.blogName=userBlog['blogName']
        
        return userBlogObj
    
    def _filterUserInfo(self,userInfo):
        userInfoObj=UserInfo()
        
        userInfoObj.url=userInfo['url']        
        userInfoObj.userID=userInfo['userid']
        userInfoObj.firstName=userInfo['firstname']
        userInfoObj.lastName=userInfo['lastname']
        userInfoObj.email=userInfo['email']
        userInfoObj.nickName=userInfo['nickname']
        
        return userInfoObj
        
    
    def getRecentPosts(self,numberOfPosts=5):
        try:
            posts=self._server.metaWeblog.getRecentPosts(self.blogID,self.userName,self.passWord,numberOfPosts)
            for post in posts:
                yield self._filterPost(post)
        except xmlrpclib.Fault, fault:
            raise MSMetaWeblogException(fault)
        
    def newPost(self,content,published):
        self._server.allow_none=True
        rv=self._server.metaWeblog.newPost(self.blogID,self.userName,self.passWord,content,published)
        return rv
    
    def editPost(self,postid,content,published):
        rv=self._server.metaWeblog.editPost(postid,self.userName,self.passWord,content,published)
        return rv
    
    def deletePost(self,postid,published,appKey=''):
        rv=self._server.blogger.deletePost(appKey,postid,self.userName,self.passWord,published)
        
    def getUsersBlogs(self,appKey=''):
        userBlogs=self._server.blogger.getUsersBlogs(appKey,self.userName,self.passWord)
    
        for userBlog in userBlogs:
            yield self._filterUserBlog(userBlog)
    
    def getUserInfo(self,appKey=''):
        userInfo=self._server.blogger.getUserInfo(appKey,self.userName,self.passWord)
        return self._filterUserInfo(userInfo)
    
    def getPost(self,postid='1'):
        return self._filterPost(self._server.metaWeblog.getPost(postid,self.userName,self.passWord))
    
    def getCategories(self):
        Categories=self._server.metaWeblog.getCategories(self.blogID,self.userName,self.passWord)
        
        for category in Categories:
            yield self._filterCategory(category)
        
