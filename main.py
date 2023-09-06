import os,json,requests
import openai
from requests.auth import HTTPBasicAuth

newsKey = os.environ["newsAPIkey"]
country = "pl"
newsUrl = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={newsKey}"

openai.api_key = os.environ["openaiAPIkey"]
openai.organization = os.environ['organisationID']
openai.Model.list()

clientID = os.environ['clientID']
clientSecret = os.environ['client_secret']

spotifyAutUurl = "https://accounts.spotify.com/api/token"
spotifyAuthData = {"grant_type":"client_credentials"}
spotifyAuth = HTTPBasicAuth(clientID, clientSecret)

response = requests.post(url=spotifyAutUurl, data=spotifyAuthData, auth=spotifyAuth)
accessToken = response.json()["access_token"]

spotifyUrl ="https://api.spotify.com/v1/search"
spotifyHeaders = {'Authorization': f'Bearer {accessToken}'}

newsResult = requests.get(newsUrl)
newsData = newsResult.json()
count = 0 
for article in newsData["articles"]:
  prompt = f"""Summarize this text in two or three words:
  {article['title']}
  """
  openaiResponse =openai.Completion.create(model ='text-davinci-002', prompt=prompt, temperature =0, max_tokens =6)
  queryresult = (openaiResponse['choices'][0]['text'].strip())
  spotifySearch = f"?q={queryresult}%3A%20&type=track&limit=1"
  fullspotifyURL = f"{spotifyUrl}{spotifySearch}"
  spotifyresponse = requests.get(fullspotifyURL, headers=spotifyHeaders) 
  dataFromSpotify = spotifyresponse.json()
  for track in dataFromSpotify["tracks"]["items"]:
    trackName = track["name"]
    trackPreview =track["preview_url"]
  songWeGot =f"""What we looked for: {queryresult} 
  
  What we found: {trackName} 
  Link:
  {trackPreview}
  
  The original title:
  {article['title']}
  """
  print(songWeGot)
  count +=1
  if count <=5:
    continue
  else:
    break