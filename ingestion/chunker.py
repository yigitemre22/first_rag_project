def chunk_text(
            pages:str,
            chunk_size:int= 1000,
            overlap:int= 200
            )->list[str]:
    """
    split text into overlapping chunks.
    """
    if chunk_size<=0:
        raise ValueError("chunksize değeri 0 dan büyük olmalıdır")
     
    if overlap <0 or overlap >= chunk_size:
        raise ValueError("overlap değeri 0'dan büyük ve chunksize değerinden küçük olmalıdır")
   
    chunks= []
    chunk_index=1

    for page in pages:
        text=page["text"]
        page_number=page["page"]
        
        start= 0

        while start < len(text):
            chunk=text[start:start+chunk_size]
            chunks.append(
                    {
                        "page":page_number,
                        "chunk_index":chunk_index,
                        "chunk":chunk,
                    }
                )

            chunk_index+=1
            start+=chunk_size-overlap

    return chunks
