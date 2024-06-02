## A simple search engine built upon Elasticsearch and PostgreSQL

### What data will you get
Your query will be evaluated on all fields of all the documents contained in Elasticsearch

### Asking for data
Send a POST request to the server (default address is `localhost:9601`) targeting the search endpoint with this payload:<br>
` {"api_key": "api key", "query":"query"} `

Curl example:<br>
` curl -X GET -H "Content-Type: application/json" --data '{"api_key": "api key", "query":"query"}' 'http://localhost:9601/search' `

### Query format
Query is formed using keywords, AND/OR statements and parenthesis<br>
Valid expressions containing more than one keyword should be structured like this:

` <keyword | parenthesis expression> AND/OR <keyword | parenthesis espression> `

Examples of valid expressions:<br>
`milk`<br>
`milk and (chocolate or strawberry)`<br>
`milk and chocolate`<br>
`(milk or ice) and (chocolate or strawberry)`

### Installation
As you might notice everything was packed in a docker-compose project for your convenience<br>
Steps to deploy:
- Copy `.env.template` to `.env` and change it to your liking
- Run `docker compose up -d --build`
- Run `docker exec -it <yourprojectname>-backend-1 python keygen.py` to get yourself a fresh API Key
- Head to `localhost:5601` to access Kibana and add some data
- Enjoy your tiny search engine!
