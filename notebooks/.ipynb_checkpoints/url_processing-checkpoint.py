import concurrent.futures

def process_url_chunk(url_chunk):
    """
    Function to process a chunk of URLs using multithreading.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads_per_process) as executor:
        return list(executor.map(featurize_url, url_chunk))
