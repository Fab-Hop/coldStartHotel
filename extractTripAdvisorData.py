#!/usr/bin/env

import pandas as pd
import numpy as np
import itertools
import rdflib
from rdflib.namespace import RDF, SDO, OWL

def readTripAdvisorData(filepath):
    tripAdvisorDf = pd.read_csv(filepath, sep='|', names=range(18)) 
    tripAdvisorDf.rename(columns={0:'ReviewDate',1:'id', 2:'hotelId', 3:'rating', 4:'reviewTitle', 5:'reviewText', 6:'stayTimeType', 7:'detailedRating', 8:'UserLocation', 9:'userRole', 10:'hotelLocation', 11:'type', 12:'services', 13:'price', 14:'14', 15:'15', 16:'hotelDescription', 17:'17'},inplace=True)
    # group reviews by hotels
    hotelDf = tripAdvisorDf[tripAdvisorDf['type']=="Hotel"][['hotelId','hotelLocation', 'services', 'price', 'hotelDescription']].groupby('hotelId').agg(set)

    # merge ammenities of all reviews (should be the same)
    hotelDf['ammenities'] = [[xx for xx in x if xx==xx] for x in hotelDf['services']]
    hotelDf['ammenities'] = [';'.join(x).split(';') if len(x) > 0 else {} for x in hotelDf['ammenities']]
    hotelDf['ammenities'] = [{xx.strip() for xx in x} for x in hotelDf['ammenities']]
    
    hotelDf['price'] = [ next(iter(x)) if len(x)>0 else np.nan for x in hotelDf['price']]
    return hotelDf

def createGraph(hotelDf, outputFilepath):

    ammenitySet = set(itertools.chain(*hotelDf.dropna(subset=['ammenities'])['ammenities']))

    #SDO = rdflib.Namespace('http://schema.org/')
    EX = rdflib.Namespace('http://example.org/')

    graph=rdflib.Graph()
    graph.bind('SDO', SDO)
    graph.bind('RDF', RDF)
    graph.bind('EX', EX)
    graph.bind('OWL',OWL)
    
    ammenityDict = dict()
    
    # create ammenity instances
    for i,x in enumerate(ammenitySet):
        ammenityURI = rdflib.URIRef(EX +'tripAdviserAmmenity'+ "%02d" % (i,))
        graph.add((ammenityURI, RDF.type, SDO.LocationFeatureSpecification))
        graph.add((ammenityURI, SDO.value, rdflib.Literal(x, lang="en")))
        ammenityDict[x] = ammenityURI
    
    hotelDf.reset_index(inplace=True)
    for i,x in hotelDf.iterrows():
        # create hotel instancess
        hotelURI = rdflib.URIRef(EX + x['hotelId'])
        graph.add((hotelURI, RDF.type, SDO.Hotel ))
    
        # set price property
        if x['price'] == x['price']:  
            graph.add((hotelURI, SDO.priceRange  ,rdflib.Literal(x['price'])))
    
        # set amenityFeature property
        for xx in ammenityDict.keys():
            if xx in x['ammenities']:
                graph.add((hotelURI, SDO.amenityFeature, ammenityDict[xx]))
            else:# set negated property instantiation
                negativeProperty = rdflib.BNode()
                graph.add((negativeProperty, RDF.type, OWL.NegativePropertyAssertion))
                graph.add((negativeProperty, OWL.sourceIndividual, hotelURI))
                graph.add((negativeProperty, OWL.assertionProperty,SDO.amenityFeature ))
                graph.add((negativeProperty, OWL.targetIndividual, ammenityDict[xx]))
    
    # write graph
    graph.serialize(destination=outputFilepath, format='n3')

def main():
    createGraph(readTripAdvisorData('data/tripadvisor.csv'),'data/tripadvisor.ttl')

if __name__ == "__main__":
    main()
