import requests, csv, json,httplib
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
today = datetime.date.today()
today = str(today)
product_line ="women_jackets"
def get_data(links, brand, y):
    print y
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
         "(KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36")
    driver = webdriver.PhantomJS(desired_capabilities = dcap,service_args=['--ignore-ssl-errors=true', '--load-images=false'])
    # driver.get(links)
    try:
        r = requests.get(links)
        response = r.status_code
        print response
        if response == 200:
            driver.get(links)
            print links

        # driver = webdriver.Chrome()

            driver.implicitly_wait(5)
            try:
                driver.find_element_by_class_name("size-buttons-show-size-chart").click()
                driver.implicitly_wait(10)
                sleep(5)
                div_s = driver.find_elements_by_class_name("size-chart-cell")
                size_data = ''
                for s in div_s:
                    temp = (str(s.get_attribute("textContent")))
                    # print temp
                    size_data += str(str(temp + " "))
                size_data2 = []
                div1 = driver.find_elements_by_class_name("size-chart-row")
                for i in range(len(div1)):
                    temp = str(div1[i].get_attribute("textContent"))
                    size_data2 += [(temp + " ")]
                ldata = (len(size_data2) + 1)

                div = driver.find_elements_by_class_name("size-chart-cell")
                da = []
                for i in range(len(div)):
                    temp = (str(div[i].get_attribute("textContent")))
                    da += [temp]

                ldata2 = len(da)
                ldata3 = ldata2 / ldata
                if ldata3 == 0:
                    print "No Data avaliable"
                    file = open(product_line+"log.txt", "a")
                    file.write("NO PROPER DATA TO PROCESS" + ", " + link[z] + ", " + brand_name[z] +", "+product_line+","+today+ "\n")
                    file.close()
                    return
                if ldata2 % ldata !=0:
                    print "NO PROPER DATA TO PROCESS"
                    file = open(product_line+"log.txt", "a")
                    file.write("NO PROPER DATA TO PROCESS" + ", " + link[z] + ", " + brand_name[z] +", "+product_line+","+today+ "\n")
                    file.close()
                    return

                # print ldata, ",", ldata2, ",", ldata3
                # print da
                arr = []
                keys = []
                values = []
                count = 0
                for i in range(0, len(da), ldata3):
                    # print i
                    keys.append(da[i])
                    values.append([])
                    values[count].append(da[i + 1]);
                    j = i + 1
                    for j in range(j, j + ldata3 - 2, 1):
                        # brand_obj[da[i]].append(da[j + 1]);
                        values[count].append(da[j + 1]);

                    count += 1
                # print keys
                # print values
                obj_list =[]

                for j in range(0,ldata3 -1) :
                    obj = {}
                    for i in range(0,len(keys)):
                        obj[keys[i]] = values[i][j]
                    obj_list.append(obj)

                # print obj_list
                # print len(obj_list)
                # # # print size_chart
                dict1 = {"product_line_name":product_line,
                        "brand_name":brand,
                        "size_chart":obj_list
                }
                #
                driver.close()
                driver.quit()
                #os.system('taskkill /f /im phantomjs.exe')
                # print dict1
                return dict1
                # json.dump(dict1, f)


            except NoSuchElementException:
                print "NoSuchElementException"
                file = open(product_line+"log.txt", "a")
                file.write("NoSuchElementException button is not available" + ", " + link[z] + ", " + brand_name[z]+", " +product_line+","+today+ "\n")
                file.close()

    except httplib.BadStatusLine:
        print "httplib.BadStatusLine"
        file = open(product_line+"log.txt", "a")
        file.write("httplib.BadStatusLine" + ", " + link[z] + ", " + brand_name[z]+", " +product_line+","+today+ "\n")
        file.close()
        # pass



brand_name = []
link = []
#will not be providing input file for this project this time
with open("brand_links_jackets_csv.csv", "r") as csvf:
    rows = csv.reader(csvf)
    for row in rows:
        brand_name.append(str(row[0]))
        temp = row[1]
        # print temp
        link.append(str(temp))
list_c= []
for z in range(0, len(link), 1):
    try:
        c = get_data(link[z], brand_name[z], z)
        list_c += [c]
        f = open(product_line+".json","w")
        json.dump(list_c, f)
        f.close()
        # print list_c
    except TimeoutException:
        file = open(product_line+"log.txt", "a")
        file.write("TimeoutException" + ", " + link[z] + ", " + brand_name[z]+", " +product_line+","+today+ "\n")
        file.close()
        print "TimeoutException"




