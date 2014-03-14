import gzip
import parser
from sys import stdout
import time
from collections import defaultdict
from posting import make_inter_posting
from merge_sort import merge_sort_write
#=======================================================================	
def read_data():
	try:	
		
		file_path = "nz2_merged/"
		page_id = 0
		start_time = time.time()
		n = 10
		for i in range(0,n):
			interim_index = defaultdict(list)
			length = 0
			start = 0
			end = 0
			doc_counter = 0
			
			gz_file_index = gzip.open(file_path + str(i) + "_index", 'rb')
			index = gz_file_index.readlines()
			gz_file_index.close()
			
			gz_file_content = gzip.open(file_path + str(i) + "_data", 'rb')
			content = gz_file_content.read()
			gz_file_content.close()
			 
			while end < len(content) and doc_counter < len(index):
				start = end
				page_details = index[doc_counter].split()
				
				url = page_details[0]
				length = int(page_details[3])
				status = page_details[6]
				
				doc_counter += 1
				page_id += 1
				end = end + length
				
				if status <> 'ok':
					continue
				
				try:
					page = content[start:end]
					pg = page
					tokenized_str = parser.parser(url, page, pg, length+1, length+1)[1]
					interim_index = make_inter_posting(interim_index, tokenized_str, page_id)
					current_time = time.time()
					stdout.write("\rPages Parsed : %i | Files Read : %i | Time Elapsed : %i secs" % (page_id, i, (current_time - start_time)))
					stdout.flush()
				except TypeError as te:
					pass
					
			merge_sort_write(interim_index, i)
	except Exception as e:
		print "Error in Reading Data : " + str(e)
		gz_file_index.close()
		gz_file_content.close()
#=======================================================================				
#GLOBAL VARIABLES
separator = '=' * 80 + '\n'
#=======================================================================	
def main():
	read_data()
#=======================================================================	
if __name__ == "__main__":
	main()
#=======================================================================
	
