import os, json
import utils
import uscode
import traceback

def run(options):
  title_number = options.get('title', None)
  # section = options.get('section', None)
  year = options.get('year', 2011)  # default to 2011 for now

  if not title_number:
    utils.log("Supply a 'title' argument to parse a title.")
    return

  filename = utils.title_filename(title_number, year)
  if not os.path.exists(filename):
    utils.log("This title has not been downloaded.")

  title = uscode.title_for(filename)

  sections = title.sections()

  count = 0
  for section in sections:
    section_number = section.enum()
    section_name = section.name()
    section_citation = u"usc/{}/{}".format(title_number, section_number)
    
    # this could probably be black boxed a little further?
    try:
        bb = section.body_lines()
        xx = uscode.GPOLocatorParser(bb)
        qq = xx.parse()
    
        section_inner_output = qq.json()
        section_outer_output = {'title': title_number,
                                'number': section_number,
                                'citation': section_citation,
                                'name': section_name,
                                'data': section_inner_output                            
                                }
        output = section_outer_output
    
        utils.write(
          json.dumps(output, sort_keys=True, indent=2),
          uscode_output(year, title_number, section_number)
        )
    
        count += 1
    except Exception, E:
        print("")
        print(u"Parsing {}.".format(section_citation))        
        print(traceback.format_exc(E))
        continue

  print "\nParsed %s sections of title %s." % (count, title_number)


def uscode_output(year, title, section):
  return "%s/%s/%s/%s.json" % (utils.output_dir(), year, title, section)
