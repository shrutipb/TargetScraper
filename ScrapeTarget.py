
import os
import requests
import urllib.request
import re,json


def CallTargetAPI():
    s= requests.session()
    s.get('https://www.target.com');
    key=s.cookies['visitorId']
    print(key)

    my_location='55144'
    # product_id='77464001'
    product_id='81204099'
    # product_id='80859208'
    #print('https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile'%(my_location,key))
    location_info = requests.get('https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile'%(my_location,key)).json()
    print(location_info)

    my_store_id = location_info[0]['locations'][0]['location_id']
    print(my_store_id)

    url = 'https://redsky.target.com/web/pdp_location/v1/tcin/%s' %product_id

    payload = {'pricing_store_id' : my_store_id, 'key': key}

    # jsondata = requests.get(url, params=payload)
    jsondata = requests.get(url)
    print(jsondata)


def GetDataByHtml(url):

    try:

        ProductInfo={'URL':url}
        fp=urllib.request.urlopen(url)
        mybytes=fp.read()
        mystr=mybytes.decode("utf8")

        title = re.findall('title data-react-helmet=.*>(.*?)Target<.title>',mystr)
        if len(title) >= 1:
            ProductInfo.update({'title': title[0]})
        else:
            ProductInfo.update({'title': ''})
        PriceCurrency = re.findall('"priceCurrency":"(.*?)"',mystr)
        if len(PriceCurrency) >= 1:
            ProductInfo.update({'PriceCurrency': PriceCurrency[0]})
        else:
            ProductInfo.update({'PriceCurrency': ''})

        preselect = re.findall('"preselect":"(.*?)"',mystr)
        if len(PriceCurrency) >= 1:
            ProductInfo.update({'preselect': preselect[0]})
        else:
            ProductInfo.update({'preselect': ''})

        data=re.findall('<div class="styles__StyledCol-sc-ct8kx6-0 jOZqCG h-padding-h-tight">(.*?)class="styles__StyledCol-sc-ct8kx6-0 yqCvw">',mystr)

        description= re.findall('Description<\/h3><div class="h-margin-v-default">(.*?)<\/div>',data[0])
        if len(description) >= 1:
            ProductInfo.update({'description': description[0]})
        else:
            ProductInfo.update({'description': ''})

        TCIN = re.findall('TCIN<\/b>:.*?>(.*?)<hr\/>',data[0])
        if len(TCIN) >= 1:
            ProductInfo.update({'TCIN': TCIN[0]})
        else:
            ProductInfo.update({'TCIN': ''})

        UPC= re.findall('UPC<\/b>:.*?>(.*?)<hr\/>',data[0])
        if len(UPC) >= 1:
            ProductInfo.update({'UPC': UPC[0]})
        else:
            ProductInfo.update({'UPC': ''})

        ProductType={}

        if len(data)>=1:
            info = re.findall('<div><div><B>(.*?):<\/B>(.*?)<\/div>', data[0])
            if len(info)>=1:
                for Detail in info:
                    ProductType.update({Detail[0]:Detail[1]})

        ProductInfo.update({'Specs':ProductType})

        JsonData=json.dumps(ProductInfo)

        CurrentPath = os.getcwd()
        # print(CurrentPath )
        Filepath= os.path.join(CurrentPath,'ProductDetail.json')
        with open(Filepath,'w') as fileObj:
            fileObj.write(JsonData)

        return ProductInfo
    except Exception as e:
        return e


print(GetDataByHtml('https://www.target.com/p/toddler-girls-shaelyn-molded-footbed-sandals-cat-jack/-/A-81204099?preselect=80859208#lnk=sametab'))







