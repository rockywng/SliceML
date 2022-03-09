import requests
pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'


def try_site(link):
    # check if link is actually a youtube link
    # https://www.youtube.com/watch?v=v8o_hA2eMzI
    if not (link[0:32] == "https://www.youtube.com/watch?v="):
        #print("linkfail")
        return False         
    request = requests.get(link)
    return False if pattern in request.text else True


print(try_site("https://www.youtube.com/watch?v=69420imcool"))
print(try_site("https://www.youtube.com/watch?v=v8o_hA2eMzI"))
print(try_site("https://stackoverflow.com/questions/68818442/how-to-check-if-a-youtube-video-exists-using-python"))