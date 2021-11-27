from PIL import Image
import random
import json
import pathlib
import os
import PIL


def genChances():
    global attributes

    for attribute in attributes:
        attributeAssets = attributes[attribute]

        chancesArray = []
        for asset in attributeAssets:
            assetChance = [asset] * attributeAssets[asset]
            chancesArray += assetChance

        attributes[attribute] = chancesArray


def genMetaTemplate():
    global metaTemplate

    metaTemplate['name'] = config['name']
    metaTemplate['symbol'] = config['symbol']
    metaTemplate['description'] = config['description']
    metaTemplate['seller_fee_basis_points'] = config['seller_fee_basis_points']
    metaTemplate['properties']['creators'] = config['creators']


def nftGenMeta(meta, i, attributesMeta):
    meta['attributes'] = attributesMeta
    meta['name'] = meta['name'] + ' ' + '#' + str(i)
    meta['image'] = f'{i - startIndex}.png'
    meta['properties']['files'][0]['uri'] = f'{i - startIndex}.png'

    return meta


with open('./metaTemplate.json') as file:
    metaTemplate = json.load(file)

with open('./config.json') as file:
    config = json.load(file)

outDir = config['outDir']
# create outDir folder if not exists
pathlib.Path(outDir).mkdir(parents=True, exist_ok=True)

attributes = config['attributes']
generatedAttributes = []

genChances()
genMetaTemplate()

amount = config['amount']
startIndex = config['startIndex']
width = config['width']
height = config['height']

i = startIndex

while i != amount + startIndex:
    meta = metaTemplate.copy()

    nftImage = Image.new('RGBA', [width, height])
    attributesMeta = []

    for attr in attributes:

        assets = attributes[attr]
        pickedAsset = random.choice(assets)

        if pickedAsset == 'empty':
            continue
        assetImg = Image.open(
            f'./assets/{attr}/{pickedAsset}.png').convert("RGBA")
        nftImage.paste(assetImg, (0, 0), assetImg)

        pickedAsset = pickedAsset.replace('_', ' ').capitalize()
        attr = attr.capitalize()

        if attr == 'hero':
            continue
        attributesMeta.append({
            "trait_type": attr,
            "value": pickedAsset
        })

    meta = nftGenMeta(meta, i, attributesMeta)

    if attributesMeta in generatedAttributes:
        continue

    generatedAttributes.append(attributesMeta)

    height, width = nftImage.size

    nftImage = nftImage.resize((height, width), Image.ANTIALIAS)

    nftImage.save(f'{outDir}/{i - startIndex}.png',
                  'PNG', optimize=True)
    with open(f'{outDir}/{i - startIndex}.json', 'w') as outfile:
        json.dump(meta, outfile)

    i += 1

with open(f'./gened.json', 'w') as outfile:
    json.dump(generatedAttributes, outfile)
