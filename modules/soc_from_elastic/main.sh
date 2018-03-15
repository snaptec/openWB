
#Abfrage an ein Elasticsearch, zurückgegeben wird der reine Soc. !!Abfrage individuell anpassen!!


#SOC in Prozent aus elasticsearch
	dpsoc=$(curl --connect-timeout 10 -s -XGET "http://localhost:9200/pid2105/_search" -H 'Content-Type: application/json' -d'
	{
	    "query": {
	        "match_all": {}
	    },
	    "size": 1,
	  "sort": [
	    {
	      "timestamp": {
	        "order": "desc"
	      }
	    }
	  ]
	}' |sed 's/^.*"socDisplay/"socDisplay/' |sed 's/,.*//' |cut -c 14- | cut -f1 -d".")

	#zur weiteren verwendung im webinterface
	echo $dpsoc > /var/www/html/openWB/ramdisk/soc
	echo $dpsoc
