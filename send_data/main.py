import falcon
import json
import pickle
import send_data
import json
from falcon_cors import CORS    
cors = CORS(allow_origins_list=['*'])  
app = falcon.API(middleware=[cors.middleware])
public_cors = CORS(allow_all_origins=True)
class TestResource(object):
	cors=public_cors
    def on_post(self, req: falcon.Request, resp: falcon.Response):
        data =str(req.stream.read().decode("utf-8"))
       # print(data['tid'])
       	new_data,data={'api':0,'data':0,'limit':1},data.split("&")
       	for i in range(len(data)):
       		data[i]=data[i].split("=")
       		new_data[data[i][0]]=data[i][1]
        resp.status = falcon.HTTP_200  # This is the default status
        #send_data.main(data)
        #resp.send('Hello')
        print(new_data)
        api=new_data['api']
        try:
        	with open('secure_token.pickle','rb') as f:
        		data=pickle.load(f)
        	if api in data:
        		print(new_data['data'])
        		#resp.media='Valid Request'
        		ree=send_data.main(new_data['data'],new_data['limit'])
        		print(ree)
        		resp.media=json.dumps(ree)
        	else:
        		resp.media=json.dumps({"Available":3})
        except Exception as e:
        	print({"Available":4})


# Instantiate the TestResource class
test_resource = TestResource()

# Add a route to serve the resource
app.add_route('/getdata', test_resource)