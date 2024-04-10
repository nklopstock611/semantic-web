import json
import texts_analytics as ta

def create_json(metadata: dict) -> None:
    for each_article in metadata:
        with open('/workspaces/semantic-web/second-task/metadata4.json', 'r') as f:
            json_dict = json.load(f)

        json_dict.update({ each_article: metadata[each_article] })

        with open('/workspaces/semantic-web/second-task/metadata4.json', 'w') as f:
            json.dump(json_dict, f)

def main():
    with open('/workspaces/semantic-web/first-task/metadata3.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    for each_paper in metadata:
        print('Extracting Metadata From', metadata[each_paper]['paper_title'])
        new_data = ta.get_analytics_json(metadata[each_paper], each_paper)
        print('Got Metadata!')
        # print(metadata)
        create_json(new_data)

if __name__ == '__main__':
    main()
