To be used for version management of the SPARQL queries and CP4 evaluation.

##CP4 Evaluation

### SUBMISSION FORMAT:


For this SPARQL query: 

	1592 - Please find and list all of the ads in Fargo, ND for Spas or Massage Parlors that offer sex services. In the answer field note the full name of the spa and/or the street address for each ad. If both address and business name are provided, note each separated by a comma. Return the least frequently occurring business.
      
    PREFIX qpr: <http://istresearch.com/qpr>
    SELECT ?business  (count(?ad) AS ?count)(group_concat(?ad;separator=',') AS ?ads)   WHERE {
        ?ad a qpr:Ad ;
        qpr:location 'Fargo, ND' ;
        qpr:business_type ?bt .
        FILTER(?bt = 'Spa' || ?bt = 'Massage Parlor')
        ?ad qpr:services 'sex' .
         qpr:business ?business .
        GROUP BY ?business
        ORDER BY ?count
        


The submission format should be normalized to:

	{
	"question_id": 1592,
	"answer": ["Some_Business, 123 ABC Street"],
	"ads":["67B8EE67F7CE5D38EC231DFD05E38D82E2067AC5E62FD7317A5D386CF2074C40",
         "77B8EE67F7CE5D38EC231DFD05E38D82E2067AC5E62FD7317A5D386CF207CCC",
         "87B8EE67F7CE5D38EC231DFD05E38D82E2067AC5E62FD7317A5D386CF2074DDD"]
     }
 
Where,
 "question_id" is the question number, 
 "answer" is an array of answer(s) or an empty array if no answer required for a query, and 
 "ads" are the _ids associated with the results.
 
 
 
### Standardization Format for Submission:
	* Email : joannacandoit@workplace.com
	* Phone : xxxx-xxxxxx
	* Address : 123 Make Way, Secret Town, CA 12575
	* Price : 80,120,100,50
	* Name : Joanna Candoit
