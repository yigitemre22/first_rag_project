from collections import defaultdict

def reciprocal_rank_fusion(*result_lists,k=60):
    """
        result_lists:
        [
            vector_results,
            keyword_results
        ]
    """

    scores=defaultdict(float)
    documents={}

    for results in result_lists:
        for rank,row in enumerate(results,start=1):

            doc_id=row[0]

            documents[doc_id]=row

            scores[doc_id]+=1/(k+rank)


    merged=sorted(
        documents.values(),
        key=lambda row:scores[row[0]],
        reverse=True,
    )

    return merged