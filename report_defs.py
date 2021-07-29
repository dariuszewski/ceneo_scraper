#converting functions
import pprint, json, csv, io
import xml.etree.ElementTree as e



def report_pydict(dataset):
    return str(dataset) #str needed for next function


def report_json(dataset):
    return json.dumps(dataset, ensure_ascii=False, indent=4)


def report_csv(dataset):
    report = io.StringIO()
    writer = csv.writer(report, quoting=csv.QUOTE_NONNUMERIC)
    headers = ['id'] + list(dataset[list(dataset.keys())[0]].keys())
    writer.writerow(headers)

    for item in dataset:
        data = [item] + list(dataset[item].values())
        writer.writerow(data)

    return report.getvalue()


def xml_report(dataset):
    report = io.StringIO()
    report.write('<report>\n')
    for key in dataset.keys():
        report.write(f'\t<product id=\"{key}\">\n')
        for k, v in dataset[key].items():
            report.write(f"\t\t<{str(k).replace(' ', '_')}>\"{v}\"</{str(k).replace(' ', '_')}>\n")
        report.write('\t</product>\n')
    report.write('</report>')

    return report.getvalue()


def txt_short_report(dataset):

    report = io.StringIO()
    report.write(f"|        id | {' '*27}name |   price | score | avability |\n")
    report.write("="*77+'\n') #77/77
    for key in dataset:
        try:
            long_name = dataset[key]['name'][:31]
        except:
            long_name = dataset[key]['name']
        report.write('| '+key+' | ' + long_name.strip().rjust(31)
+ ' | ' + str(dataset[key]['price']).rjust(7) + ' | '
+ str(dataset[key]['score']).rjust(5) + ' | '
+ str(dataset[key]['avability']).rjust(9) + ' |\n' )

    return report.getvalue()
