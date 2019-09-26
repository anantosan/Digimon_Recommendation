from flask import Flask, jsonify, request, render_template,redirect
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

app= Flask(__name__)

@app.route('/')
def beranda():
    return render_template('search_digi.html')

@app.route('/hasil',methods=['POST'])
def hasil():
    search=request.form
    dig_chose=search['nama'].lower()
    data=df[['no','digimon','image','stage','type','attribute']]
    data['digimon']=data['digimon'].str.lower()
    def combine_features(data):
        return data['stage']+"/"+data['type']+"/"+data['attribute']
    data["combined_features"] = data.apply(combine_features,axis=1)
    cv = CountVectorizer(tokenizer=lambda i:i.split('/'))
    count_matrix = cv.fit_transform(data['combined_features'])
    cosine_sim= cosine_similarity(count_matrix)
    data_digi=list(data['digimon'])
    if dig_chose not in data_digi:
        return render_template('error_digi.html')
    else:
        dig_chose_img=data['image'].loc[data['digimon']==dig_chose].values[0]
        index_chose=data[data['digimon']==dig_chose].index.values[0]
        digi=list(enumerate(cosine_sim[index_chose]))
        sort_digimon=sorted(digi, key=lambda i:i[1], reverse=True)
        list_digi=[]
        list_pic=[]
        list_feature=[]
        for i in sort_digimon[:7]:
            if data.iloc[i[0]]['digimon']!=dig_chose:
                list_digi.append(data.iloc[i[0]]['digimon'])
                list_pic.append(data.iloc[i[0]]['image'])
                a=[]
                a.append(data.iloc[i[0]][['stage','type','attribute']])
                list_feature.append(a)
        return render_template('hasil_digi.html',data=list_digi, pilihan=dig_chose,pic=list_pic,pic_chose=dig_chose_img,feature=list_feature)


if __name__=='__main__':
    df=pd.read_json('digimon.json')
    app.run(debug=True)