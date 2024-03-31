def buildFrame(data):
    """ """
    reformat = {}
    keys = [k for k, v in data[0].items()]
    for key in keys:
        reformat[key] = list()
    for org in data:
        for key in keys:
            reformat[key].append(org.get(key, ""))
    frame = pd.DataFrame(data)
    frame.to_csv('test.csv', encoding='utf-8')
    return frame
    
    # idList = [v for org in data for k, v in org.items() if k == 'id']