import twitter

username = 'twitter-user'
password = 'twitter-pass'

login = True

if login:
    api=twitter.Api(username,password)
else:
    api=twitter.Api()

msg = 'twitter python ok'
status = api.PostUpdate(msg)
print status.text
