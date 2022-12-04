from flask import Flask
import boto3
import numpy as np

app = Flask(__name__)
app.env = "development"


@app.route('/convertRecommend', methods=['GET'])
async def home():
    s3_downLoad = boto3.client('s3')
#s3.meta.client.download_file("sagemaker-ap-southeast-1-946249623096", "data/train.npy", 'train.npy')
    input = s3_downLoad.get_object(Bucket='sagemaker-ap-southeast-1-946249623096', Key='data/input.txt')
    contents = input['Body'].read()
    data = np.genfromtxt(contents.splitlines(),dtype=None)
    output = np.save('output.npy', data)
    test = np.load('output.npy')
    
    session = boto3.Session(
    aws_access_key_id= 'AKIA5YUG7MY4FAGFW4MP',
    aws_secret_access_key= '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')
    s3 = session.resource('s3')
    s3.meta.client.upload_file('output.npy', 'sagemaker-ap-southeast-1-946249623096', "data/train4.npy")
    
    # object = s3.Object('sagemaker-ap-southeast-1-946249623096', 'data/train3.npy')
    # result = object.put(Body=test)

    print('contents', test)
    return {"message": "upload successfully!"}


@app.route('/recommendProduct', methods=['POST'])
async def recommendProduct():
    return {
        "productList": str([1,2,3,21,22,23])
        }

if __name__ == '__main__':
    app.run(port=8081,debug= True)

# pip install flask==2.1.3 --user
# pip install flask[async] --user