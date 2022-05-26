====================
 planet api instructions
 ====================
 
 ============================================
 Build or Pull :  if you want to build yourself please follow steps 1 to 4 , else go to step 5
 ============================================
 
 1) Go to your work dir where you may want to clone the code in
 for ex : cd myfolder
 
 2) clone the repo
 git clone git@github.com:ctalpade/planet-assignment.git
 
 3) change dir to planet-assignment
 cd planet-assignment
 
 4) build the image
 docker build --tag ctalpade/planet_userapi_img:v1 .
 
 5) If you want to use existing image  , pull the image on the machine where you want to run.
 docker pull ctalpade/planet_userapi_img:v1
 
 ============================================
 Running the container based on the image
 ============================================
 1) run the container
 docker container run -d -p 5000:5000 --env DBPATH=/app --env DBFILENAME=test.db --name planet_userapi_testcont ctalpade/planet_userapi_img:v1
 
 2) check the logs
 docker logs --follow planet_userapi_testcont
 
 ============================================
 Testing the container 
 ============================================
 1) Test the api using testclient
 docker exec --env DBPATH=/app --env DBFILENAME=test.db -ti planet_userapi_testcont  sh -c "python client/testclient.py"
 
 2) Test the api using Postman app.
 You can also test the api using postman app by importing the postman collection json.
 It will provide all the end points that can be tested for the API.
 
 ============================================
 Cleanup the container and image
 ============================================
 1) docker container stop planet_userapi_testcont
 2) docker container rm planet_userapi_testcont
 3) docker image rm ctalpade/planet_userapi_img:v1