from pdf_reader import read_pdf

def chunk_text(text:str,
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
    start= 0

    while start < len(text):
        chunk=text[start:start+chunk_size]
        chunks.append(chunk)
        start+=chunk_size-overlap

    return chunks
