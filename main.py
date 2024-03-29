import requests
from urllib.parse import urlparse
import json
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, jsonify, request, send_from_directory
import os
import json

#app flask mak api function
app = Flask(__name__)

# Create the ThreadPoolExecutor outside the fast_download function.
executor = ThreadPoolExecutor()

@app.route('/', methods=['GET'])
def home():
    return """<!DOCTYPE html>
<html>
<head>
    <style>
        /* CSS styles */
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 20px;
        }

        h1 {
            color: #333;
            font-size: 24px;
        }

        p {
            color: #666;
            font-size: 16px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 4px;
            padding: 30px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .api-link {
            color: #007bff;
            text-decoration: none;
        }

        .api-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>How to Use this API?</h1>
        <p>
            To use the API, make a GET request to the following URL:
            <br>
            <a href="https://webpage.com/apii?url=(pdf_url)" class="api-link">https://webpage.com/apii?url=(pdf_url)</a>
        </p>
        <p>
            Replace "(pdf_url)" in the URL with the actual URL of the PDF file you want to retrieve data from.
        </p>
    </div>
</body>
</html>
"""

def check_if_video_exists(videoURL):
    try:
        response = requests.head(videoURL)
        return response.status_code == 200  
    except requests.RequestException:
        return False
    
def numereda(url):
    try:
        payload = {}
        headers = {
        'authority': 'www.numerade.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_scid=1217b3ef-4ec4-4f26-ac4d-015640c8c7a4; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-622355-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; optiMonkClientId=38e05ccd-50f4-701b-dbb4-336c3d4a870a; _pin_unauth=dWlkPU1tTTVaV0UyWXprdFltWmxNaTAwTlRBeUxXSmhObVF0WXpWa1ltUmhZelU1WWpOaQ; _hjSessionUser_1309276=eyJpZCI6IjVmZTI5MDgzLWUxZTgtNTZlMy1hZWNmLTI5ODlhMTQ0ZTY0MyIsImNyZWF0ZWQiOjE2ODEyODkwOTUwMTIsImV4aXN0aW5nIjp0cnVlfQ==; _tt_enable_cookie=1; _ttp=4nklKmRR_fX8L6ENxXfC8NsiggF; csrftoken=J3l3kLEHkMqxhFQIdMWNGkcSoaunkuNXR8uaoc8PVE8uxZne8NXTbPlxMwIqmyQE; sessionid=pqw58q70f39aj3xakalt61778s1zv7z9; _sctr=1%7C1681842600000; crisp-client%2Fsession%2F05e623e1-dc7c-4a29-ada6-d433aa94b258=session_f2d73657-e338-48db-92e2-1dd63f44fc83; _gcl_au=1.1.1112083136.1697465262; _scid_r=1217b3ef-4ec4-4f26-ac4d-015640c8c7a4; _gid=GA1.2.2120702992.1697465263; _rdt_uuid=1697465263395.0820ad1e-57b6-4b8c-930d-526e6da98a9a; _ga=GA1.1.1590358435.1681289092; _ga_K0NSFP2V8T=GS1.1.1697465263.7.0.1697465264.59.0.0; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2250cd4a06-c513-432e-97be-71e74b1383d2%22%2C%22options%22%3A%7B%22end%22%3A%222024-11-16T14%3A07%3A44.529Z%22%2C%22path%22%3A%22%2F%22%7D%7D; _hjIncludedInSessionSample_1309276=0; _hjSession_1309276=eyJpZCI6IjExOGMxMDliLWEzZTUtNDM1Yy1iNTU1LTM4YzkyYWExMWE1MSIsImNyZWF0ZWQiOjE2OTc0NjUyNjY1NDQsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6dHJ1ZX0=; csrftoken=gY51Lxju8jvxtYFLHZjOET6pCgXECF0aPMOr4qx9MmX71bNOi3fKzOuBlspVJrv7; sessionid=ejay63sxwip9xkhrj4ooi8f2prtdfhv8',
        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(response.status_code)
        if response.status_code == 200:
            try:
                question_container = soup.find('div', class_='ask-question-detail__question-container')
                question_text = question_container if question_container else None
                image = soup.find('img', class_='ask-img')
                image_url = image['src'] if image else None
                question_html = f'({question_text}<img src="{image_url}" alt="question_image">)'
                element_to_scrape = soup.find('div', {'id': 'steps-container'})
                element_string = str(element_to_scrape)
                img_tag = soup.find("img", class_="background-gif")
                if img_tag:
                    img_src = img_tag["src"]
                    print(img_src)
                    parts = img_src.split('/')
                    desired_part = parts[-1].split('_')[0]
                    print(desired_part)
                    videoURL = ""
                    if desired_part:
                       videoURL = f"https://cdn.numerade.com/project-universal/encoded/{desired_part}.mp4"
                       if not check_if_video_exists(videoURL):
                          videoURL = f"https://cdn.numerade.com/ask_video/{desired_part}.mp4"
                    if not videoURL:
                       videoURL = f"https://cdn.numerade.com/ask_video/{desired_part}.webm"      


                responsevideoURL = requests.request("GET", videoURL)
                if responsevideoURL.status_code == 200:
                    print(videoURL)
                    answerhtml=str("""<!DOCTYPE html> <html> <head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <title>NX pro</title> <meta name="description" content=""> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="shortcut icon" type="image/x-icon" href="assets/img/favicon.ico"> <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css"> <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.min.js"></script> </head> <body> <div class="container"> <div id="app"> <div class="container"> <div class="section"> <div class="box" style="word-break: break-all;"> <h1>Question Link</h1> <div class="url">"""+str(url)+"""</div></div> <div class="box"> <div class="content"> <h1>Question</h1> <div class="question">"""+str(question_html)+"""</div> </div> </div> <div class="box"> <div class="content"> <h1>Answer</h1> <div class="answer"></div>"""+str(element_string)+"""<br><h1>VEDIO LINK: <a href="""""+str(videoURL)+""""">"""+str(videoURL)+"""</a></h1><br><video width="500" controls><source src="""+str(videoURL)+""" type="video/mp4"></video></div> </div> </div> </div> </div> </div> <script type="text/x-mathjax-config">MathJax.Hub.Config({ config: ["MMLorHTML.js"], jax: ["input/TeX","input/MathML","output/HTML-CSS","output/NativeMML"], extensions: ["tex2jax.js","mml2jax.js","MathMenu.js","MathZoom.js"], TeX: { extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js"] } });</script> <script type="text/javascript" src="https://cdn.mathjax.org/mathjax/2.0-latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script></body> </html>""")
                else:
                    print(videoURL)
                    answerhtml=str("""<!DOCTYPE html> <html> <head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <title>NX pro</title> <meta name="description" content=""> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="shortcut icon" type="image/x-icon" href="assets/img/favicon.ico"> <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css"> <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.min.js"></script> </head> <body> <div class="container"> <div id="app"> <div class="container"> <div class="section"> <div class="box" style="word-break: break-all;"> <h1>Question Link</h1> <div class="url">"""+str(url)+"""</div></div> <div class="box"> <div class="content"> <h1>Question</h1> <div class="question">"""+str(question_html)+"""</div> </div> </div> <div class="box"> <div class="content"> <h1>Answer</h1> <div class="answer"></div>"""+str(element_string)+"""<br><h1>VEDIO LINK: <a href="""""+str(videoURL)+""""">"""+str(videoURL)+"""</a></h1><br><video width="500" controls><source src="""+str(videoURL)+""" type="video/mp4"></video></div> </div> </div> </div> </div> </div> <script type="text/x-mathjax-config">MathJax.Hub.Config({ config: ["MMLorHTML.js"], jax: ["input/TeX","input/MathML","output/HTML-CSS","output/NativeMML"], extensions: ["tex2jax.js","mml2jax.js","MathMenu.js","MathZoom.js"], TeX: { extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js"] } });</script> <script type="text/javascript" src="https://cdn.mathjax.org/mathjax/2.0-latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script></body> </html>""")
            except Exception as e:
               print(f"An error occurred: {e}")
               question_container = soup.find('div', class_='video-redesign-subheader')
               question_html  = question_container.find('p').text.strip()
               img_tag = soup.find("img", class_="background-gif")
               if img_tag:
                img_src = img_tag["src"]
                print(img_src)
                parts = img_src.split('/')
                if 'jpg' in img_src:
                    desired_part = parts[-1].split('_')[0]
                elif 'gif' in img_src:  
                    desired_part = parts[-1].split('.')[0]
                    print(desired_part)
                    if 'jpg' in img_src:
                       videoURL =f"https://cdn.numerade.com/project-universal/encoded/{desired_part}.mp4"
                    elif 'gif' in img_src:
                       videoURL =f"https://cdn.numerade.com/encoded/{desired_part}.mp4"
                responsevideoURL = requests.request("GET", videoURL)
                if responsevideoURL.status_code==200:
                   print(videoURL)
                   answerhtml=str("""<!DOCTYPE html> <html> <head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <title>NX pro</title> <meta name="description" content=""> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="shortcut icon" type="image/x-icon" href="assets/img/favicon.ico"> <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css"> <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.min.js"></script> </head> <body> <div class="container"> <div id="app"> <div class="container"> <div class="section"> <div class="box" style="word-break: break-all;"> <h1>Question Link</h1> <div class="url">"""+str(url)+"""</div></div> <div class="box"> <div class="content"> <h1>Question</h1> <div class="question">"""+str(question_html)+"""</div> </div> </div> <div class="box"> <div class="content"> <h1>Answer</h1> <div class="answer"></div><h2>Answer Vedio:-</h2><br><h1>VEDIO LINK: <a href="""+str(videoURL)+""">"""+str(videoURL)+"""</a></h1><br><video width="500" controls><source src="""+str(videoURL)+""" type="video/mp4"></video></div> </div> </div> </div> </div> </div> <script type="text/x-mathjax-config">MathJax.Hub.Config({ config: ["MMLorHTML.js"], jax: ["input/TeX","input/MathML","output/HTML-CSS","output/NativeMML"], extensions: ["tex2jax.js","mml2jax.js","MathMenu.js","MathZoom.js"], TeX: { extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js"] } });</script> <script type="text/javascript" src="https://cdn.mathjax.org/mathjax/2.0-latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script></body> </html>""")
                else:
                   print(videoURL)
                   answerhtml=str("""<!DOCTYPE html> <html> <head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <title>NX pro</title> <meta name="description" content=""> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="shortcut icon" type="image/x-icon" href="assets/img/favicon.ico"> <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css"> <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.min.js"></script> </head> <body> <div class="container"> <div id="app"> <div class="container"> <div class="section"> <div class="box" style="word-break: break-all;"> <h1>Question Link</h1> <div class="url">"""+str(url)+"""</div></div> <div class="box"> <div class="content"> <h1>Question</h1> <div class="question">"""+str(question_html)+"""</div> </div> </div> <div class="box"> <div class="content"> <h1>Answer</h1> <div class="answer"></div><h2>Answer Vedio:-</h2><br><h1>VEDIO LINK: <a href="""""+str(videoURL)+""""">"""+str(videoURL)+"""</a></h1><br><video width="500" controls><source src="""+str(videoURL)+""" type="video/mp4"></video></div> </div> </div> </div> </div> </div> <script type="text/x-mathjax-config">MathJax.Hub.Config({ config: ["MMLorHTML.js"], jax: ["input/TeX","input/MathML","output/HTML-CSS","output/NativeMML"], extensions: ["tex2jax.js","mml2jax.js","MathMenu.js","MathZoom.js"], TeX: { extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js"] } });</script> <script type="text/javascript" src="https://cdn.mathjax.org/mathjax/2.0-latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script></body> </html>""")
            return answerhtml
        else:
           return '<h4>400 Not found vedio</h4>'
    except Exception as e:
       print(f"An error occurred: {e}")


@app.route('/apii', methods=['GET'])
def process_slideshare_api():
  try:  
    with app.app_context():
        url = request.args.get('url')
        if url:
            result = numereda(url)
            return result
        else:
            return f'your question mite be not answered\n\nQuestion link : {url}'
  except Exception as e :
    print(f"An error occurred: {e}")    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
