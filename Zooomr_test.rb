#This work is licenced under http://creativecommons.org/licenses/GPL/2.0/

require 'Zooomr'

zooomr = ZooomrRestAPI.new('api-key', 'sharekey')

token = 'tokenstring'

frob = zooomr.auth.getFrob()

# check to see if we need to get authorisation
response = zooomr.auth.checkToken('auth_token' => token)
response = false

if (false.eql?(response))
    
  link_hash = zooomr.authenticate_application('perms' => "write")

  puts "Follow this to authenticate: " + link_hash['link']

  gets
  puts 'Authorize Succed!'
  
  info_hash = zooomr.complete_authentication('frob' => link_hash['frob'])
  json_resp = info_hash.json_response
  token = json_resp['auth']['_content']['token']
    

  user      = json_resp['auth']['_content']['user']
  user_id   = user['nsid']
  username  = user['username']
  fullname  = user['fullname']
  
  puts "NSID: " + user_id + ", USERNAME: " + username + ", FULLNAME: " + fullname
  
else
  
  json_resp = response.json_response
  token = json_resp['auth']['_content']['token']
    

  user      = json_resp['auth']['_content']['user']
  user_id   = user['nsid']
  username  = user['username']
  fullname  = user['fullname']
  
  puts "NSID: " + user_id + ", USERNAME: " + username + ", FULLNAME: " + fullname
  
end

#token = info_hash['auth']['_content']['token']
# test
params = { 'param_name' => "param_value"}
zooomr.test.echo(params)

zooomr.test.login('auth_token' => token)


# test the upload
image_path = '/home/user/NationPhoto/2008-11-07/moken-fisherman-reynard-965471-xl.jpg'
zooomr.upload.uploadPhoto('filename' => image_path, 'auth_token' => token)

# test zipline
zooomr.zipline.postLine('status' => "Testing zipline from the Zooomr API", 'auth_token' => token, 'is_public' => false, 'is_friend' => false, 'is_family' => false)
zooomr.zipline.getLine('auth_token' => token)
