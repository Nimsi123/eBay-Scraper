#from Ebay.ItemOrganization.ProductList import ProductList
from Ebay.ItemOrganization.queryList import queryList
from Ebay.ItemOrganization.Client import Client
from Ebay.Site_Operations.ebayFunctions_Grand import aboutALink
from name_collection import *

"""
DESCRIPTION OF HIGH LEVEL OPERATIONS

process of downloading html and iterating over pages
   request the link and download the html
   scrape data from the html
   export the data

process of importing and displaying the data
   import the data into a series of ProductList() objects
   per ProductList() object, graph its contents
   print all the graphs into a single pdf sheet
"""
#set up the web request client

from scraper_api import ScraperAPIClient
#client = ScraperAPIClient('c733663048589db82005534b6739c32e') #nimsi@berkeley.edu
#client = ScraperAPIClient('cbbdd094d7401d8912b09341e37be9b1') #nimarahmanian8@gmail.com
#client = ScraperAPIClient('bfb3cb210e50c39d09f82432095a5150') #nimarahmanian2020@gmail.com
client = Client

def whack_shit():
    """
    Print the total number of collected items. How many items are we tracking for every product? How big is the sample size?

    NOTE: THIS METHOD WILL NEED TO BE CHANGED. IMPORTPRODUCTDATA AND EXPORTPRODUCTDATA HAVE BEEN DELETED.
    """
    lengthList = []
    count = 0
    for query in totalQueries.queryCollection:
        length = 0

        query.importProductData(query.csv_Auction)
        length += len(query.product_collection.item_list)

        query.importProductData(query.csv_BIN)
        length += len(query.product_collection.item_list)
        #lengthList.append(length)

        if length < 500:
            print(f"{query.name:<30}{length}")
            count += 1

def test_export_function(client, totalQueries):
    """
    Does the export_item_data function work as intended?
    """


    query = totalQueries.queryCollection[0]
    print("collecting: ", query.name)

    length_of_auction_list, length_of_csv = [], [] # a list of numbers. the numbers represent the size of each list as the for loop cycles.

    for i in range(4):

        #data for Auction listings
        print(f"\n{query.name} AUCTION")
        temp_list = ProductList()
        aboutALink(client, query.linkAuction, temp_list)

        #after we populate temp_list
        length_of_auction_list.append( len(temp_list.item_list) )

        export_list = ProductList()
        temp_list.export_item_data(query.csv_Auction, export_list)

        #after we populate the csv file
        length_of_csv.append( len(export_list.item_list) )

        print("length for AUCTION", len(temp_list.item_list))

    print(length_of_auction_list)
    print(length_of_csv)
    print("finished data collection")


#totalQueries = data_import()
#data_collection(client, totalQueries)
#test_export_function(client, totalQueries)
#data_visualization(totalQueries)


totalQueries = queryList()

#totalQueries.add_new_queries(The_Beatles)
#totalQueries.add_new_queries(Cream)
#totalQueries.remove_old_queries(Cream)

#[print(query.name) for query in totalQueries.queryCollection[320:]]
#print(totalQueries.find_count("PlayStation 5"))
totalQueries.data_collection(client, start_index = 210, single_search = True)
#totalQueries.data_visualization(start_index = 0, single_graph = True)