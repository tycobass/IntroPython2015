import getopt
import sys

filename_listing = 'Directory_crawler_listing.txt'
log_file = 'Directory_crawler_log.txt'

print ('ARGV      :', sys.argv[1:])

options, remainder = getopt.getopt(sys.argv[1:], 'f:l:', ['filename_listing=', 
                                                                                'log_file=', 
                                                                                ])

for opt, arg in options:
    if opt in ('-f', '--filename_listing'):
        filename_listing = arg
    elif opt in ('-l', '--log_file'):
        log_file = arg

print ('filename_listing   :', filename_listing)
print ('log_file   :', log_file)
print ('sys.argv[5]    :', sys.argv[5])
print ('args :', remainder)