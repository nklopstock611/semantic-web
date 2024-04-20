import json
import texts_analytics as ta

new_metadata_path = '/semantic-web/second-task/metadata_keywords.json'
metadata_path = '/semantic-web/first-task/metadata4.json'

def create_json(metadata: dict) -> None:
    """
    Updates a json file.
    """
    for each_article in metadata:
        with open(new_metadata_path, 'r') as f:
            json_dict = json.load(f)

        json_dict.update({ each_article: metadata[each_article] })

        with open(new_metadata_path, 'w') as f:
            json.dump(json_dict, f)

def main():
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    # if the download is interrupted, you can start from a specific paper
    starting_key = 'Managing User Focused Access to Distributed Knowledge'
    start_processing = False 
    count = 0

    for each_paper in metadata:
        count += 1
        current_title = metadata[each_paper].get("paper_title", "")
        if not start_processing:
            if current_title == starting_key:
                print(count)
                start_processing = True
            else:
                continue

        print('Extracting Metadata From', current_title)
        new_data = ta.get_analytics_json(metadata[each_paper], each_paper)
        print('Got Metadata!')
        # print(metadata)
        create_json(new_data)

if __name__ == '__main__':
    main()
