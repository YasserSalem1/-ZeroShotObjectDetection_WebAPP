import requests, json, shutil

basr_url = 'http://localhost:5000/'
files = {'query_img': open('ahmed.jpg', 'rb')}
response = requests.post(f'{basr_url}/yasser', files=files)

data = json.loads(response.text)
img_path = data.get('img_path', '')
predictions = data.get('predictions', [])

print(img_path)
for x in predictions:
    print(x)


res2 = requests.get(f'{basr_url}/getImg?imgId={img_path}', stream=True)
file = open(img_path, 'wb')
res2.raw.decode_content = True
shutil.copyfileobj(res2.raw, file)



# Extract the predictions from the response
# predictions_json = response.json().get('predictions')

# Print the predictions
# print(predictions_json)

