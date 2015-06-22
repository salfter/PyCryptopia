#!/usr/bin/env python
# coding=iso-8859-1

# PyCryptopia: a Python binding to the Cryptopia API
#
# based on PyCryptsy; implements the subset of functionality the
# Cryptopia API currently exposes
#
# Copyright © 2013-2015 Scott Alfter
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


import pycurl
import time
import hashlib
import urllib
import StringIO
import json

class PyCryptopia:
  
  # constructor
  def __init__(self):
    pass
    
  # issue any supported query (method: string)
  def Query(self, method):
    # generate GET URL
    url="https://www.cryptopia.co.nz/api/"+method

    # curl handle
    b=StringIO.StringIO()
    ch=pycurl.Curl()
    ch.setopt(pycurl.URL, url)
    ch.setopt(pycurl.SSL_VERIFYPEER, 0)
    ch.setopt(pycurl.WRITEFUNCTION, b.write)
    try:
      ch.perform()
    except pycurl.error, error:
      errno, errstr=error
      raise Exception("pycurl error: "+errstr)
  
    # decode and return
    try:
      rtnval=json.loads(b.getvalue())
    except:
      raise Exception("unable to decode response")
    return rtnval

  # get market ID (return None if not found)
  def GetMarketID (self, src, dest):
    try:
      r=self.Query("GetTradePairs")
      for i, market in enumerate(r["Data"]):
        if market["Symbol"].upper()==src.upper() and market["BaseSymbol"].upper()==dest.upper():
          mkt_id=market["Id"]
      return mkt_id
    except:
      return None
    
  # get market IDs for a destination currency
  def GetMarketIDs (self, dest):
    try:
      rtnval={}
      r=self.Query("GetTradePairs")
      for i, market in enumerate(r["Data"]):
        if market["BaseSymbol"].upper()==dest.upper():
          rtnval[market["Symbol"].upper()]=market["Id"]
      return rtnval
    except:
      return None
    
  # get buy price for a market ID
  def GetBuyPriceByID (self, mktid):
    try:
      r=self.Query("GetMarketOrders/"+str(mktid))
      return float(r["Data"]["Buy"][0]["Price"])
    except:
      return 0

  # get sell price for a market ID
  def GetSellPriceByID (self, mktid):
    try:
      r=self.Query("GetMarketOrders/"+str(mktid))
      return float(r["Data"]["Sell"][0]["Price"])
    except:
      return 0

  # get buy price for a currency pair
  def GetBuyPrice (self, src, dest):
    return self.GetBuyPriceByID(self.GetMarketIDs(dest)[src])

  # get sell price for a currency pair
  def GetSellPrice (self, src, dest):
    return self.GetSellPriceByID(self.GetMarketIDs(dest)[src])

