import requests

headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'referer': 'https://www.udemy.com/courses/search/?src=ukw&q=python'
}
for i in range(1,  4):
    url_api= 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p=' + str(i)

    respuesta= requests.get(url_api, headers= headers)

    data=respuesta.json()

    cursos=data["courses"]

    for curso in cursos:
        print("#"*50)
        print(curso["title"])
        print(curso["num_reviews"])
        print(curso["rating"])


