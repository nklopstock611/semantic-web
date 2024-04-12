import json
import texts_analytics as ta

new_metadata_path = '/home/estudiante/semantic-web/second-task/metadata_keywords.json'
metadata_path = '/home/estudiante/semantic-web/first-task/metadata4.json'

def create_json(metadata: dict) -> None:
    for each_article in metadata:
        with open(new_metadata_path, 'r') as f:
            json_dict = json.load(f)

        json_dict.update({ each_article: metadata[each_article] })

        with open(new_metadata_path, 'w') as f:
            json.dump(json_dict, f)

def main():
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    for each_paper in metadata:
        print('Extracting Metadata From', metadata[each_paper]['paper_title'])
        new_data = ta.get_analytics_json(metadata[each_paper], each_paper)
        print('Got Metadata!')
        # print(metadata)
        create_json(new_data)

if __name__ == '__main__':
    main()
