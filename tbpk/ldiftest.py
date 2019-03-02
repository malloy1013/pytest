import ldif3
class testParser(ldif3.LDIFParser):
    def __init__(self,input_file,ignored_attr_types=None,max_entries=0,process_url_schemes=None,line_sep='\n' ):
      ldif3.LDIFParser.__init__(self,input_file,ignored_attr_types,max_entries,process_url_schemes,line_sep)



f = open('cygwin.ldif','r')
ldif_parser = testParser(f).handle
ldif_parser
