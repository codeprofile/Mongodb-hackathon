# GDELT Flask based event/news data display

Here GDELT data is extracted using `gdeltdoc` library and after extracting data is passed on to UI and inserted into the MongoDB .

<img src="https://user-images.githubusercontent.com/94001814/170778639-8693ba38-a96f-40eb-a1d1-d11c9d2f3f1c.gif">


<b><u> Steps to Run this Project :</u> </b>
<ul>
  <li> run >> `git clone https://github.com/codeprofile/Mongodb-hackathon` </li>
  <li> cd till >> `Mongodb-hackathon`  </li>
  <li> run >> `pip install -r requirements.txt` </li>
  <li> run >> `flask run` </li>
  </ul>
  
<b> FYI : </b>
script will always take today's (script run date) as start_date and yesterday's as end_date and we are only trying to capture English Language event data from gdelt .
